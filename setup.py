from setuptools import setup, find_packages

APP_NAME = 'photo-uploader'
APP_DIR = 'photo_uploader'
VERSION_STRING = None

with open('%s/version.py' % APP_DIR) as version:
  for line in version:
    if line.startswith('__version__'):
      VERSION_STRING = line.strip().split('=')[1]

setup(
    name=APP_NAME,
    version=VERSION_STRING,
    packages=find_packages(),
    include_package_data=True,
    long_description=__doc__,
    entry_points={
        'console_scripts': [
            '%s = %s.%s:main' % (APP_NAME, APP_DIR, APP_DIR),
        ]
    },
)
