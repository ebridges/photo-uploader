from os import path
from logging import basicConfig, INFO, DEBUG
from hashlib import md5
from functools import partial
from pathlib import Path
from magic import Magic


SUPPORTED_EXTENSIONS = (
    '.jpg', '.jpeg', '.png', '.mov', '.mp4'
)


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


def valid_type(item):
  ext = Path(item.lower()).suffix
  return ext in SUPPORTED_EXTENSIONS


def md5sum(filename, block_size=2**20):
  '''
  Returns MD5 checksum for given file.
  '''
  with open(filename, mode='rb') as file:
    d = md5()
    for buf in iter(partial(file.read, block_size), b''):
      d.update(buf)
  return d.hexdigest()


def mime_type(filename):
  '''
  Returns the mime type of the given file.
  '''
  mime = Magic(mime=True)
  return mime.from_file(filename)


def read_item_data(filename):
  '''
  Returns the bytes of the given file as a buffer.
  '''
  with open(filename, "rb") as binary_file:
      # Reads the whole file at once
      return binary_file.read()

