'''
Photo Uploader
Usage:
  photo-uploader auth --credentials-file=<PATH> [--verbose]
  photo-uploader user-info --credentials-file=<PATH> [--verbose]
  photo-uploader upload --credentials-file=<PATH> --image=<PATH_TO_IMAGE [--verbose]
  photo-uploader -h | --help
  photo-uploader --version
Options:
  --credentials-file=<PATH> File containing auth credentials.
  --image=<PATH_TO_IMAGE>   Path to an image to upload.
  -h --help                 Show this screen.
  --version                 Show version.
  --verbose                 Debug-level output.
'''

from logging import info, error

from docopt import docopt
from .smugmug_service import SmugMugService
from .version import __version__
from .util import configure_logging, item_folder
from .auth_util import get_auth_tokens, update_credentials
from .upload_util import get_folder_info, upload


def upload_item(credentials_file, item):
  info('upload() called.')
  service = SmugMugService(credentials_file)
  folder = item_folder(item)
  if folder:
    folder_info = get_folder_info(service, folder)
    info('folder info:\n%s' % folder_info)
    success = upload(service, folder_info, item)
    if success:
      info('successfully uploaded [%s]' % item)
    else:
      error('error uploading [%s]' % item)


def auth(credentials_file):
  info('auth() called.')
  access_token, access_token_secret = get_auth_tokens(credentials_file)
  update_credentials(credentials_file, access_token, access_token_secret)
  info('access token updated in [%s]' % credentials_file)


def user_info(credentials_file):
  service = SmugMugService(credentials_file)
  print(service.user_info())


def main():
  args = docopt(__doc__, version=__version__)
  configure_logging(args['--verbose'])

  credentials_file = args['--credentials-file']

  if args['auth']:
    auth(credentials_file)

  if args['user-info']:
    user_info(credentials_file)

  if args['upload']:
    image = args['--image']
    upload_item(credentials_file, image)
