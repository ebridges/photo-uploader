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

from .version import __version__
from .util import configure_logging
from .auth_util import API_ORIGIN, get_service, add_auth_params, update_credentials, open_session

from logging import info, debug
from docopt import docopt
import sys


def auth(credentials_file):
  info('auth() called.')
  service = get_service(credentials_file)
  rt, rts = service.get_request_token(params={'oauth_callback': 'oob'})
  auth_url = add_auth_params(
            service.get_authorize_url(rt), access='Full', permissions='Modify')
  print('Go to %s in a web browser.' % auth_url)
  sys.stdout.write('Enter the six-digit code: ')
  sys.stdout.flush()
  verifier = sys.stdin.readline().strip()  
  at, ats = service.get_access_token(rt, rts, params={'oauth_verifier': verifier})

  print('Access token: %s' % at)
  print('Access token secret: %s' % ats)

  update_credentials(credentials_file, at, ats)
  info('access token updated in [%s]' % credentials_file)


def user_info(credentials_file):
  session = open_session(credentials_file)
  print(session.get(
    API_ORIGIN + '/api/v2!authuser',
    headers={'Accept': 'application/json'}).text)
  
  
def main():
  args = docopt(__doc__, version=__version__)
  configure_logging(args['--verbose'])

  credentials_file = args['--credentials-file']

  if(args['auth']):
    auth(credentials_file)
    
  if(args['user-info']):
    user_info(credentials_file)
    
