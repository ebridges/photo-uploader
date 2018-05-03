from logging import info, error
from .smugmug_service import get_node_path


def get_folder_info(service, folder):
  '''
  Given a folder for a media object return info about it,
  creating the folder & its parent if necessary.
  '''
  folders = folder.split('/')
  user_info = service.user_info()
  current_folder = None
  parent_folder = get_node_path(user_info)
  for f in folders:
    current_folder = '%s/%s' % (current_folder, f)
    info('current_folder: %s' % current_folder)
    info('parent_folder: %s' % parent_folder)
    current_folder_info = service.folder_info(parent_folder['Uri'], current_folder)
    if not current_folder_info:
      error('Folder: %s not found' % folder)
      current_folder_info = service.create_folder(parent_folder, '/%s' % f)
      info('Folder created: %s' % current_folder_info)
    parent_folder = current_folder_info
  info('folder_info for %s:\n%s' % (current_folder, current_folder_info))
  return current_folder_info
