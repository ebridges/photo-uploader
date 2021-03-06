import sys
import json
from logging import error, info
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode
from rauth import OAuth1Service, OAuth1Session
from cachecontrol import CacheControl
from cachecontrol.caches.file_cache import FileCache

OAUTH_ORIGIN = 'https://secure.smugmug.com'
REQUEST_TOKEN_URL = OAUTH_ORIGIN + '/services/oauth/1.0a/getRequestToken'
ACCESS_TOKEN_URL = OAUTH_ORIGIN + '/services/oauth/1.0a/getAccessToken'
AUTHORIZE_URL = OAUTH_ORIGIN + '/services/oauth/1.0a/authorize'

API_ORIGIN = 'https://api.smugmug.com'


def get_auth_tokens(credentials_file):
  service = get_service(credentials_file)
  request_token, request_token_secret = service.get_request_token(params={'oauth_callback': 'oob'})
  auth_url = add_auth_params(
      service.get_authorize_url(request_token), access='Full', permissions='Modify')
  info('Open this URL: [%s]' % auth_url)
  sys.stdout.write('Enter the six-digit code: ')
  sys.stdout.flush()
  verifier = sys.stdin.readline().strip()
  return service.get_access_token(request_token, request_token_secret,
                                  params={'oauth_verifier': verifier})


def update_credentials(credentials_file, access_token, access_token_secret):
  config = None
  with open(credentials_file, 'r') as c_f:
    config = json.load(c_f)
    config['access_token'] = access_token
    config['access_token_secret'] = access_token_secret
  with open(credentials_file, 'w') as c_f:
    json.dump(config, c_f)


def get_service(credentials_file):
  try:
    with open(credentials_file, 'r') as c_f:
      config = json.load(c_f)
  except IOError as io_error:
    print('====================================================')
    print('Failed to open credentials.json! Did you create it?')
    print('The expected format is demonstrated in example.json.')
    print('====================================================')
    error('exception: %s' % io_error)
    sys.exit(1)

  if isinstance(config) is not dict \
     or 'client_key' not in config \
     or 'client_secret' not in config\
     or isinstance(config['client_key']) is not str \
     or isinstance(config['client_secret']) is not str:
    print('====================================================')
    print('Invalid credentials.json!')
    print('The expected format is demonstrated in example.json.')
    print('====================================================')
    sys.exit(1)

  return OAuth1Service(
      name='smugmug-oauth-web-demo',
      consumer_key=config['client_key'],
      consumer_secret=config['client_secret'],
      request_token_url=REQUEST_TOKEN_URL,
      access_token_url=ACCESS_TOKEN_URL,
      authorize_url=AUTHORIZE_URL,
      base_url=API_ORIGIN + '/api/v2')


def add_auth_params(auth_url, access=None, permissions=None):
  if access is None and permissions is None:
    return auth_url
  parts = urlsplit(auth_url)
  query = parse_qsl(parts.query, True)
  if access is not None:
    query.append(('Access', access))
  if permissions is not None:
    query.append(('Permissions', permissions))
  return urlunsplit((
      parts.scheme,
      parts.netloc,
      parts.path,
      urlencode(query, True),
      parts.fragment))


def init_session(credentials_file):
  access_token = None
  access_token_secret = None
  client_key = None
  client_key_secret = None
  with open(credentials_file, 'r') as c_f:
    config = json.load(c_f)
    access_token = config['access_token']
    access_token_secret = config['access_token_secret']
    client_key = config['client_key']
    client_key_secret = config['client_secret']

  session = OAuth1Session(
      client_key,
      client_key_secret,
      access_token=access_token,
      access_token_secret=access_token_secret)

  return CacheControl(session, cache=FileCache('.web_cache'))
