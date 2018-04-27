from .auth_util import init_session

API_ORIGIN = 'https://api.smugmug.com'

class SmugMugService():
  def __init__(self, credentials_file):
    self.session = init_session(credentials_file)


  def user_info(self):
    return self.session.get(
      API_ORIGIN + '/api/v2!authuser',
      headers={'Accept': 'application/json'}).text

  def root_node():
    pass

