from logging import info, warn, debug
from .smugmug_service import get_node_path


def get_folder_info(service, folder):
  '''
  Given a folder for a media object return info about it,
  creating the folder & its parent if necessary.
  '''
  info('get_folder_info(%s)' % folder)
  folders = folder.strip('/').split('/')
  user_info = service.user_info()
  current_folder = ''
  parent_folder = get_node_path(user_info)
  for folder_part in folders:
    current_folder = '%s/%s' % (current_folder, folder_part)
    info('current_folder: [%s] / parent_folder: [%s]' % (current_folder, parent_folder))
    current_folder_info = service.folder_info(parent_folder, current_folder)
    if not current_folder_info:
      warn('Creating folder: [%s] because it is not found' % folder_part) #pylint: disable=W1505
      current_folder_info = service.create_folder(parent_folder, folder_part)
    parent_folder = current_folder_info
  debug('folder_info for %s:\n%s' % (current_folder, current_folder_info))
  return current_folder_info


def upload(service, album, item):
  '''
  Given an item (an image or video), upload it into the given album.
  '''
  info('folder_info: [%s], image[%s]' % (album, item))
  return None
