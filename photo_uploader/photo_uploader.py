'''
Photo Uploader
Usage:
  photo-uploader auth --credentials-file=<PATH> [--verbose]
  photo-uploader user-info --credentials-file=<PATH> [--verbose]
  photo-uploader upload --credentials-file=<PATH> [--verbose]
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
from .auth_util import get_auth_tokens, update_credentials
from .upload_util import get_folder_info  # upload
# from .data_util import query_by_workflow, 
# update_workflow, SYNCHRONIZED, UPLOADED

from logging import info
from docopt import docopt


def upload(credentials_file):
    info('upload() called.')
    service = SmugMugService(credentials_file)
    get_folder_info(service, '2017/2017-02-02')

# ALT: don't query a db for the list, pass a list in by param
# def upload(credentials_file):
#   info('upload() called.')
#   service = SmugMugService(credentials_file)
#   to_upload = query_by_workflow(SYNCHRONIZED)
#   for item in to_upload:
#     item_folder = item_folder(item)
#     info('uploading item [%s]' % item)
#     folder_info = get_folder_info(service, item_folder)
#     upload(service, folder_info, item)
#     info('item [%s] uploaded' % item)
#     update_workflow(item, UPLOADED)
#     info('workflow updated for [%s' % item)


def auth(credentials_file):
    info('auth() called.')
    at, ats = get_auth_tokens(credentials_file)
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
    
    if(args['upload']):
        upload(credentials_file)
