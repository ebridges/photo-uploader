import os
import sys
import re
from enum import Enum
from logging import info, debug, error
from requests import exceptions
from .auth_util import init_session
from .util import md5sum, mime_type, read_item_data

API_ORIGIN = 'https://api.smugmug.com'


def h(add_headers=None): #pylint: disable=C0103
  '''
  Generates standard headers for a request, with option to add more.
  '''
  headers = {'Accept': 'application/json'}
  if add_headers:
    for key in add_headers:
      debug('Adding header [%s] to request' % key)
      headers[key] = add_headers[key]
  return headers


def upload_headers(album_uri, item):
  '''
  Given an `item` create all headers containing information
  required to upload it to an `album`.
  '''
  file_size = os.path.getsize(item)
  file_type = mime_type(item)
  md5_sum = md5sum(item)
  headers = {
      'Content-MD5': md5_sum,
      'Content-Type': file_type,
      'Content-Length': file_size,
      'X-Smug-AlbumUri': album_uri,
      'X-Smug-ResponseType': 'JSON',
      'X-Smug-Version': 'v2'
  }
  return h(headers)


def u(path): #pylint: disable=C0103
  '''
  Binds a path to the host part to create a URL.
  '''
  debug('Creating URL for path [%s]' % path)
  return '%s%s' % (API_ORIGIN, path)


def get_node_path(folder_info):
  '''
  Gets a node from a blob of JSON from the API.
  '''
  response = folder_info['Response']

  if 'User' in response:
    return response['User']['Uris']['Node']
  else:
    return folder_info['Uri']


def get_node_for_folder(folder_info, folder):
  if 'Response' not in folder_info:
    raise ValueError('Expected a `Response` element in Node JSON.')

  if 'Node' not in folder_info['Response']:
    info('Folder [%s] does not exist as a child of [%s]' % (folder, folder_info['Response']['Uri']))
    return None

  nodes = folder_info['Response']['Node']
  info("nodes: %s" % nodes)
  for node in nodes:
    info(">>node: %s" % node)
    if node['UrlPath'] == folder:
      return node
  return None


def get_node_type(folder):
  for ntype in NodeType:
    if ntype.regex().match(folder):
      return ntype.smugmug_ordinal()
  return None

class NodeType(Enum):
  ALBUM = (4, r'^\d{4}-\d{2}-\d{2}$')
  FOLDER = (2, r'^\d{4}$')

  def __init__(self, ordinal, regex):
    self.ordinal = ordinal
    self.pattern = re.compile(regex)

  def regex(self):
    return self.pattern

  def smugmug_ordinal(self):
    return self.ordinal


class SmugMugService():
  def __init__(self, credentials_file):
    self.session = init_session(credentials_file)


  def user_info(self):
    return self.session.get(u('/api/v2!authuser'),
                            headers=h()).json()


  def folder_info(self, parent, folder):
    '''
    For a given `folder` name, get its node from its `parent`.
    '''
    info('getting folder info for: %s' % folder)
    parent_node_uri = parent['Uri']
    folder_info = self.session.get(u('%s!children' % parent_node_uri),
                                   headers=h()).json()
    node_info = get_node_for_folder(folder_info, folder)
    debug('got folder node: %s' % node_info)
    return node_info


  def create_folder(self, parent, folder):
    '''
    Given a `folder` create it as a child of `parent`, returning
    the node info for the created folder.
    '''
    info('creating folder: [%s]' % folder)

    node_type = get_node_type(folder)
    if not node_type:
      raise ValueError('unrecognized folder name: [%s]' % folder)
    info('creating folder [%s] of type: [%d]' % (folder, node_type))

    url = u('%s!children' % parent['Uri'])
    headers = h()
    payload = {
        'Type': node_type,
        'Name': folder,
        'UrlName': folder,
        'EffectivePrivacy': 3, # Private
        'OriginalSizes' : 1,
        'Filenames' : 1
    }

    response = self.session.post(url, data=payload, headers=headers)
    try:
      response.raise_for_status()
    except exceptions.HTTPError as err:
      error(str(err))
      for key, val in response.headers.items():
        error('%s : %s' % (key, val))
      sys.exit(1)
    folder_info = response.json()
    return folder_info['Response']['Node']


  def upload_item_to_album(self, album, item):
    '''
    Given an image or video `item`, upload it to the given `album`.
    '''
    info('uploading [%s] to [%s].' % (item, album))

    url = 'https://upload.smugmug.com'
    headers = upload_headers(album['Uri'], item)
    image_data = read_item_data(item)

    response = self.session.post(
        url,
        data=image_data,
        header_auth=True,
        headers=headers
    )

    return response
