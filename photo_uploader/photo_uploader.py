'''
Photo Uploader
Usage:
  photo-uploader [--verbose]
  photo-uploader -h | --help
  photo-uploader --version
Options:
  -h --help     Show this screen.
  --version     Show version.
  --verbose     Debug-level output.
'''

from .version import __version__
from .util import configure_logging
from logging import info, debug
from docopt import docopt


def run():
  info('run() called.')


def main():
  args = docopt(__doc__, version=__version__)
  configure_logging(args['--verbose'])
  run()
