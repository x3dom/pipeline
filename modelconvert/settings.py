import os
import platform

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
#PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
path = lambda *a: os.path.join(PROJECT_ROOT, *a)

# Far too clever trick to know if we're running on the deployment server.
DEVELOPMENT_MODE = (platform.node() != "x3dom")
DEBUG = DEVELOPMENT_MODE

SECRET_KEY = '\xad\x12+\x13l\t\x811\x05\x9d\x01W\xd0?\xb9\xb61\xfe\xd5G\xe6^W\x0e'
ADMINS = frozenset(['http://x3dom.org'])

MAX_CONTENT_LENGTH = 16 * 1024 * 1024 # 16Meg upload limit

# location of the user templates (fullsize, metadata, etc.)
TEMPLATE_PATH = path('templates/bundles')

UPLOAD_PATH = '/var/www/modelconvert/tmp/uploads'
DOWNLOAD_PATH = '/var/www/modelconvert/tmp/downloads'
AOPT_BINARY = '/usr/local/bin/aopt'

ALLOWED_EXTENSIONS = set(['x3d','ply', 'x3db', 'wrl', 'bin', 'fhb', 'off',
                          'osb', 'osg', 'raw', 'slp', 'stl', 'jt', '3ds', 
                          'dae', 'dxf', 'lxo', 'obj', 'x', 'bin', 'fhb',
                          'off', 'osb', 'osg'])

#USE_X_SENDFILE = True
SERVER_NAME = 'modelconvert.x3dom.org'

# only for production debugging
PROPAGATE_EXCEPTIONS = True
#TRAP_HTTP_EXCEPTIONS = True
#TRAP_BAD_REQUEST_ERRORS = True

# redis
CELERY_RESULT_BACKEND = "redis"
CELERY_REDIS_HOST = "localhost"
CELERY_REDIS_PORT = 6379
CELERY_REDIS_DB = 0
CELERY_BROKER_URL = 'redis://localhost:6379/0'


if DEVELOPMENT_MODE:
    SERVER_NAME = 'localhost:5000'
    UPLOAD_PATH = path('../tmp/uploads')
    DOWNLOAD_PATH = path('../tmp/downloads')
    TEMPLATE_PATH = path('templates/bundles')
    AOPT_BINARY = '/Users/andi/Storage/tmp/instant_player/Contents/MacOS/aopt'

del os
del platform