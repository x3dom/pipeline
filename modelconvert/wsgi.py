"""
WSGI config for modelconvert project.

This module contains the WSGI application used by production WSGI deployments. 
It should expose a module-level variable named ``application``. 

Usually you will have the standard Flask WSGI application here, but it also
might make sense to replace the whole Flask WSGI application with a custom one
that later delegates to the Flask one. For example, you could introduce WSGI
middleware here, or combine a Flask application with an application of another
framework.

"""
import os
import sys
import pwd


# http://code.google.com/p/modwsgi/wiki/ApplicationIssues#User_HOME_Environment_Variable
os.environ['HOME'] = pwd.getpwuid(os.getuid()).pw_dir


# This is currently deployment specific and not required
# with a packaged deploy (since the package is in the Python path)
BASE_DIR = os.path.join(os.path.dirname(__file__), '..')

#activate_this = os.path.join(BASE_DIR, "venv/bin/activate_this.py")
#execfile(activate_this, dict(__file__=activate_this))

if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)


from modelconvert import create_app
application = create_app()

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)