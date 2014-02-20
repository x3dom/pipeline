"""
Default config file. 

This file is loaded first and provides sensible defaults for the
application. It also reads environment variables to allow configuration
of the app through the environment (http://www.12factor.net/config).
The following variables can currentluy be configured via environment:

    SECRET_KEY          For session generation. You absolutely need to 
                        set this in production environments. To generate
                        a key run python and type this:

                        >>> import os
                        >>> os.urandom(24)

                        There is a default, but please only use this
                        in development.

    ADMINS              A comma seperated list of Email addresses. This
                        is used to send notification emails to the 
                        app maintainers.
                        default: root@localhost

    DEBUG               Enable/disable debug mode.
                        default: False (possible: False, True)

    DOWNLOAD_PATH       Absolute path to directory that is used to
                        store generated files. The directory needs to
                        be writable by the process which owns the 
                        application. It needs to be readable by the
                        webserver. You should override the default
                        value in production.
                        default: module_dir/../tmp/downloads

    UPLOAD_PATH         Absolute path to directory which holds uploaded
                        files. This needs to be read/writable by the
                        application process. You should override the
                        default value in production.
                        default: module_dir/../tmp/uploads


    AOPT_BINARY         Absolute path to the aopt binary (including
                        executable). default: aopt (PATH lookup)

    MESHLAB_BINARY      Absolute path to the meshlabserver binary 
                        (including the executable). 
                        default: meshlabserver (PATH lookup)

    MESHLAB_DISPLAY     X11 display port for meshlabserver. Set this to
                        you default display in a non headless setup. For
                        a headless setup the default is :99, you need
                        to run a Xvfb instance there.
                        default: ':99'


    CELERY_BROKER_URL   Celery broker url
                        default: redis://localhost:6379/0


    SERVER_NAME         The name and port number of the server. 
                        Required for subdomain support (e.g.: 'myapp.dev:5000') 
                        Note that localhost does not support subdomains 
                        so setting this to "localhost" does not help. 
                        Setting a SERVER_NAME also by default enables 
                        URL generation without a request context but 
                        with an application context.
                        default: none
    
    DEFAULT_MAIL_SENDER Email address From field for outgoing emails. This 
                        setting also controls wether the mail features is active
                        or not. You need to change the default to another value
                        in order to acticate it. This is a temporary security measure.
                        default: noreply@localhost

    MAIL_SERVER         The SMTP server, default: localhost
    MAIL_PORT           The STMP port, default: 25
    MAIL_USE_TLS        Use TLS auth, default: False
    MAIL_USE_SSL        Use SSL auth, default: False
    MAIL_USERNAME       Mailserver username, default: ""
    MAIL_PASSWORD       Mailserver password, default: ""



    MAX_CONTENT_LENGTH  File upload limit in bytes. Caution: the default is very
                        loose. If a POST or PUT request exeeds this limit
                        a http 413 is returned. Tweak this to your needs but 
                        be aware that POST/PUT bombs are a common attack vector.
                        default: 134217728 (=128MB)

    ALLOWED_DOWNLOAD_HOSTS  A list of hosts which are allowed to download
                            files from. Basic secuirty for the "download model
                            from URL functionality". You need to set this with
                            the environment through a comma seperated list e.g.:
                            x3dom.modelconvert.org,someother.domain.com
                            default: localhost:5000

    BUNDLES_PATH        Where the user templates reside. Usually you 
                        don't want to override this.
                        default: module_dir/bundles

    TEMPLATE_PATH       Where the UI templates reside. 
                        default: module_dir/templates

    STATIC_PATH         Where the static assets for the UI reside. 
                        default: module_dir/static
                        
    LOGFILE             Absolute path to a file to pipe stdout logging 
                        to. This should not be used in production. 
                        default: False (stdout logging)

    DEVELOPMENT_MODE    Enable/disable dev mode. This is a old setting
                        and will be removed. Set to false in production.
                        default: False (possible: False, True)

You can also override all settings with a custom config file which 
may contain Python code. In order to do so you need to specify only one 
environment variable:

    MODELCONVERT_SETTINGS=/path/to/config.py

Note that you need to give an absolute path and that all values you
specify there override the defaults as well as OS environment set 
values.
"""
import os
import platform

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
path = lambda *a: os.path.join(PROJECT_ROOT, *a)

def env_var(key, default=None, proc=None):
    """Retrieves env vars and makes Python boolean replacements"""
    val = os.environ.get(key, default)
    if val == 'True':
        val = True
    elif val == 'False':
        val = False

    if isinstance(val, basestring):
        val = val.strip()
        
    if proc:
        val = proc(val)

    return val


# Far too clever trick to know if we're running on the deployment server.
# you need to change this if you are deploying to another host
#DEVELOPMENT_MODE = (platform.node() != "x3dom")
#DEBUG = DEVELOPMENT_MODE

DEBUG = env_var('DEBUG', False)

DEVELOPMENT_MODE = env_var('DEVELOPMENT_MODE', False)

SECRET_KEY = env_var('SECRET_KEY', '\xa9!\xea\xe9(\xd4\xae\x1c\xfb!8\x0c\xa4\xf1\xe4*\xca\xa2\xac\xf8\\\xee\x11\xad')

# this is tricky it allows a comma seperated list of values string
# as env var and converts it to a frozen set
ADMINS = env_var('ADMINS', 'root@localhost', 
                 lambda x: frozenset(x.replace(' ', '').split(',')))


MAIL_SERVER = env_var("MAIL_SERVER", "localhost")
MAIL_PORT = env_var('MAIL_PORT', "25")
MAIL_USE_TLS = env_var('MAIL_USE_TLS', False)
MAIL_USE_SSL = env_var('MAIL_USE_SSL', False)
MAIL_USERNAME = env_var('MAIL_USERNAME', "")
MAIL_PASSWORD = env_var('MAIL_PASSWORD', "")
DEFAULT_MAIL_SENDER = env_var('DEFAULT_MAIL_SENDER', "noreply@localhost")

MAX_CONTENT_LENGTH = int(env_var('MAX_CONTENT_LENGTH', 128 * 1024 * 1024)) # 16Meg upload limit

# location of the user templates (fullsize, metadata, etc.)
BUNDLES_PATH = env_var('BUNDLES_PATH', path('bundles'))

#customization of UI templates
STATIC_PATH = env_var('STATIC_PATH', path('static'))
TEMPLATE_PATH = env_var('TEMPLATE_PATH', path('templates'))


LOGFILE = env_var('LOGFILE', False)   # default logging to stdout

# FIXME: the defaults here don't correlate do the DEBUG=False default
UPLOAD_PATH = env_var('UPLOAD_PATH', path('../tmp/uploads'))
DOWNLOAD_PATH = env_var('DOWNLOAD_PATH', path('../tmp/downloads'))

AOPT_BINARY = env_var('AOPT_BINARY', 'aopt')
NEXUS_BINARY = env_var('NEXUS_BINARY', '/opt/build/nexus2.0/bin/nxsbuild')
MESHLAB_BINARY = env_var('MESHLAB_BINARY', 'meshlabserver')
MESHLAB_DISPLAY = env_var('MESHLAB_DISPLAY', ':99')

PREVIEW_URI = env_var('PREVIEW_URI', 'preview/')

# extension, description
SUPPORTED_FORMATS = (
    ('x3d', 'X3D'),
    ('x3db', 'X3D Binary'),
    ('osg', 'Open Scene Graph'),
    ('osb', 'OSB file'),
    ('3ds', '3D Studio Max'),
    ('ply', 'PLY files'),
    ('wrl', 'VRML'),
    ('bin', 'Binary'),
    ('fhb', 'FHB files'),
    ('off', 'OFF files'),
    ('raw', 'RAW files'),
    ('slp', 'SLP files'),
    ('stl', 'STL files'),
    ('jt', 'JT files'),
    ('dae', 'DAE files'),
    ('dxf', 'AutoCad files'),
    ('lxo', 'LXO files'),
    ('obj', 'Object files'),
    ('x', 'X files'),
    ('fhb', 'FHB files'),
)

SUPPORTED_META_DATA = (
    ('xml', 'XML Metadata'),
    ('txt', 'Text metadata'),
    ('json', 'JSON metadata'),
)

SUPPORTED_ARCHIVES = (
    ('zip', 'ZIP archive'),
)

SUPPORTED_MODEL_EXTENSIONS = set([ext[0] for ext in SUPPORTED_FORMATS])
SUPPORTED_META_EXTENSIONS = set([ext[0] for ext in SUPPORTED_META_DATA])
SUPPORTED_ARCHIVE_EXTENSIONS = set([ext[0] for ext in SUPPORTED_ARCHIVES])

ALLOWED_EXTENSIONS = set()
ALLOWED_EXTENSIONS.update(SUPPORTED_MODEL_EXTENSIONS)
ALLOWED_EXTENSIONS.update(SUPPORTED_META_EXTENSIONS)
ALLOWED_EXTENSIONS.update(SUPPORTED_ARCHIVE_EXTENSIONS)



# A list
ALLOWED_DOWNLOAD_HOSTS = env_var('ALLOWED_DOWNLOAD_HOSTS', 
    default='localhost:5000,x3dom.org,www.x3dom.org', 
    proc=lambda x: frozenset(x.replace(' ', '').split(','))
)



#USE_X_SENDFILE = True
if env_var('SERVER_NAME'):
    SERVER_NAME = env_var('SERVER_NAME', 'localhost:5000')

# only for production debugging
# PROPAGATE_EXCEPTIONS = True
# TRAP_HTTP_EXCEPTIONS = True
# TRAP_BAD_REQUEST_ERRORS = True


# these tasks are executed in parallel by the pipeline when conversion
# is triggered. note that those tasks run in PARALLEL if you specify
# multiple tasks and one tasks depends on the data of another task
# you need to implement this on your own. If you need a certain set of 
# tasks running in series, you need to create a controller task which
# orchestrates your sub tasks. This is exactly what we do by default.
TASKS = (
    'modelconvert.tasks.convert_model',
)

# application bundles provide output template for the render pipeline
# as well as custom python code. they are full fledged python modules
INSTALLED_BUNDELS = (
    'modelconvert.bundles.basic',
    'modelconvert.bundles.standard',
)


# -- CELERY -----------------------------------------------------------------
CELERY_RESULT_BACKEND = 'redis'
CELERY_BROKER_URL = env_var('CELERY_BROKER_URL', 'redis://localhost:6379/0')
BROKER_URL = CELERY_BROKER_URL

# FIXME: make this work with TASKS variable
CELERY_IMPORTS = ("modelconvert.tasks", )

#CELERY_TASK_RESULT_EXPIRES = 300 # default is one day
CELERY_HIJACK_ROOT_LOGGER = False
CELERYD_LOG_COLOR=False
CELERYD_MAX_TASKS_PER_CHILD=1 

# simplify log output during development
if DEBUG:
    CELERYD_LOG_FORMAT = '%(message)s'
    CELERYD_TASK_LOG_FORMAT = '%(message)s'


del os
del platform
del env_var
del path