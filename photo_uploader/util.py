from logging import basicConfig, INFO, DEBUG
from os import path

def configure_logging(level):
  if not level:
    level = INFO
  else:
    level = DEBUG
  basicConfig(
      format='[%(asctime)s][%(levelname)s][%(module)s] %(message)s',
      datefmt='%Y/%m/%d %H:%M:%S',
      level=level)


def item_folder(item):
  if not item:
    return None

  folder = path.dirname(item)

  return folder[2:] if(folder.startswith('./')) else folder
