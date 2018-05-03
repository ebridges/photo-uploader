from .auth_util import init_session

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

class SmugMugService():
  def __init__(self, credentials_file):
    self.session = init_session(credentials_file)


  def user_info(self):
    return self.session.get(u('/api/v2!authuser'), 
      headers=h()).json()

  def root_node():
    pass

