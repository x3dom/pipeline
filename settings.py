import os, platform

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
#PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
path = lambda *a: os.path.join(PROJECT_ROOT, *a)

# Far too clever trick to know if we're running on the deployment server.
DEVELOPMENT_MODE = (platform.node() != "x3dom")

DEBUG = DEVELOPMENT_MODE

SECRET_KEY = '\xad\x12+\x13l\t\x811\x05\x9d\x01W\xd0?\xb9\xb61\xfe\xd5G\xe6^W\x0e'
ADMINS = frozenset(['http://x3dom.org'])

MAX_CONTENT_LENGTH = 16 * 1024 * 1024 # 16Meg upload limit

UPLOAD_PATH = '/var/www/modelconvert/tmp/uploads'
DOWNLOAD_PATH = '/var/www/modelconvert/tmp/downloads'
AOPT_BINARY = '/usr/local/bin/aopt'

ALLOWED_EXTENSIONS = set(['x3d','ply'])

if DEVELOPMENT_MODE:
    UPLOAD_PATH = os.path.join(PROJECT_ROOT, 'tmp/uploads')
    DOWNLOAD_PATH = os.path.join(PROJECT_ROOT, 'tmp/downloads')
    AOPT_BINARY = '/Users/andi/Storage/instant_player/Contents/MacOS/aopt'

del os