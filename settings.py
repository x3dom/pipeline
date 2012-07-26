import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
#PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# set this to false in deployment
DEVELOPMENT = False  

DEBUG = DEVELOPMENT

SECRET_KEY = '\xad\x12+\x13l\t\x811\x05\x9d\x01W\xd0?\xb9\xb61\xfe\xd5G\xe6^W\x0e'
ADMINS = frozenset(['http://x3dom.org'])

MAX_CONTENT_LENGTH = 16 * 1024 * 1024 # 16Meg upload limit

UPLOAD_PATH = '/var/www/modelconvert/htdocs/uploads'
AOPT_BINARY = '/usr/local/bin/aopt'

ALLOWED_EXTENSIONS = set(['x3d','ply'])

if DEVELOPMENT:
    UPLOAD_PATH = os.path.join(PROJECT_ROOT, 'uploads')
    

del os