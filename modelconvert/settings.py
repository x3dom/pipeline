import os
import platform

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
path = lambda *a: os.path.join(PROJECT_ROOT, *a)

# Far too clever trick to know if we're running on the deployment server.
# you need to change this if you are deploying to another host
DEVELOPMENT_MODE = (platform.node() != "x3dom")
DEBUG = DEVELOPMENT_MODE

SECRET_KEY = '\xad\x12+\x13l\t\x811\x05\x9d\x01W\xd0?\xb9\xb61\xfe\xd5G\xe6^W\x0e'
ADMINS = frozenset(['admin@domain'])

MAX_CONTENT_LENGTH = 16 * 1024 * 1024 # 16Meg upload limit

# location of the user templates (fullsize, metadata, etc.)
TEMPLATE_PATH = path('templates/bundles')

UPLOAD_PATH = '/var/www/modelconvert/tmp/uploads'
DOWNLOAD_PATH = '/var/www/modelconvert/tmp/downloads'
AOPT_BINARY = '/opt/instantReality/bin/aopt'
MESHLAB_BINARY = '/opt/meshlab/meshlab/src/distrib/meshlabserver'
MESHLAB_DISPLAY = ':99'

ALLOWED_EXTENSIONS = set(['x3d','ply', 'x3db', 'wrl', 'bin', 'fhb', 'off',
                          'osb', 'osg', 'raw', 'slp', 'stl', 'jt', '3ds', 
                          'dae', 'dxf', 'lxo', 'obj', 'x', 'bin', 'fhb',
                          'off', 'osb', 'osg', 'zip', 'tar.gz', 'tar.bz2'])

#USE_X_SENDFILE = True
SERVER_NAME = 'modelconvert.x3dom.org'

# only for production debugging
PROPAGATE_EXCEPTIONS = True
#TRAP_HTTP_EXCEPTIONS = True
#TRAP_BAD_REQUEST_ERRORS = True


# -- CELERY -----------------------------------------------------------------
CELERY_RESULT_BACKEND = "redis"
CELERY_BROKER_URL = 'redis://localhost:6379/0'
BROKER_URL = CELERY_BROKER_URL
CELERY_IMPORTS = ("tasks", )
#CELERY_TASK_RESULT_EXPIRES = 300 # default is one day


# development specific stuff, should really be seperate file
if DEVELOPMENT_MODE:
    SERVER_NAME = 'localhost:5000'
    UPLOAD_PATH = path('../tmp/uploads')
    DOWNLOAD_PATH = path('../tmp/downloads')
    TEMPLATE_PATH = path('templates/bundles')
    AOPT_BINARY = path('../tmp/ir/bin/aopt')
    MESHLAB_BINARY = path('../tmp/meshlab/bin/meshlabserver')
    MESHLAB_DISPLAY = ':0'

del os
del platform
