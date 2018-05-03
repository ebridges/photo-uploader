from logging import info, warn
from .smugmug_service import get_node_path


def get_folder_info(service, folder):
  '''
  Given a folder for a media object return info about it,
  creating the folder & its parent if necessary.
  '''
  folders = folder.strip('/').split('/')
  user_info = service.user_info()
  current_folder = ''
  parent_folder = get_node_path(user_info)
  for f in folders:
    current_folder = '%s/%s' % (current_folder, f)
    info('current_folder: [%s] / parent_folder: [%s]' % current_folder, parent_folder)
    current_folder_info = service.folder_info(parent_folder['Uri'], current_folder)
    if not current_folder_info:
      warn('Creating folder: [%s] because it is not found' % folder)
      current_folder_info = service.create_folder(parent_folder, f)
    parent_folder = current_folder_info
  debug('folder_info for %s:\n%s' % (current_folder, current_folder_info))
  return current_folder_info
