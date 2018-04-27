'''
Photo Uploader
Usage:
  photo-uploader auth --credentials-file=<PATH>
  photo-uploader user-info --credentials-file=<PATH>
  photo-uploader [--verbose]
  photo-uploader -h | --help
  photo-uploader --version
Options:
  --credentials-file=<PATH> File containing auth credentials.
  -h --help                 Show this screen.
  --version                 Show version.
  --verbose                 Debug-level output.
'''

from .smugmug_service import SmugMugService
from .version import __version__
from .util import configure_logging
from .auth_util import get_auth_tokens, update_credentials, open_session

from logging import info, debug
from docopt import docopt
import sys


def auth(credentials_file):
  info('auth() called.')
  at,ats = get_auth_tokens(credentials_file)
  update_credentials(credentials_file, at, ats)
  info('access token updated in [%s]' % credentials_file)


def user_info(credentials_file):
  service = SmugMugService(credentials_file)
  print(service.user_info())
  
  
def main():
  args = docopt(__doc__, version=__version__)
  configure_logging(args['--verbose'])

  credentials_file = args['--credentials-file']

  if(args['auth']):
    auth(credentials_file)
    
  if(args['user-info']):
    user_info(credentials_file)
    
