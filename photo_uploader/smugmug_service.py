from .auth_util import init_session
from logging import info, debug

API_ORIGIN = 'https://api.smugmug.com'

def h(add_headers=None):
  headers = {'Accept': 'application/json'}
  if(add_headers):
    for key in add_headers:
      headers[key] = add_headers[key]
  return headers


def u(path):
  debug('Creating URL for path [%s]' % path)
  return '%s%s' % (API_ORIGIN, path)


def get_node_path(folder_info):
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
  for node in nodes:
    if node['UrlPath'] == folder:
      return node
  return None


def node_path(info):
  return info['Response']['User']['Uris']['Node']['Uri']


class SmugMugService():
  def __init__(self, credentials_file):
    self.session = init_session(credentials_file)


  def user_info(self):
    return self.session.get(u('/api/v2!authuser'), 
      headers=h()).json()


  def root_folder(self):
    info = self.user_info()
    return node_path(info)


  def folder_info(self, parent, folder):
    info('getting folder info for: %s' % folder)
    folder_info = self.session.get(u('%s!children' % parent), 
      headers=h()).json()
    node_info = get_node_for_folder(folder_info, folder)
    debug('got folder info: %s' % node_info)
    return node_info


  def create_folder(self, parent, folder):
    '''
    Given a `folder` create it as a child of `parent`, returning
    the node info for the created folder.
    '''
    info('creating folder: [%s]' % folder)

    url=u('%s!children' % parent['Uri'])
    headers=h()
    payload={
        'Type': 2, # "Folder" 
        'Name': folder, 
        'UrlName': folder, 
        'EffectivePrivacy': 'Private'
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
