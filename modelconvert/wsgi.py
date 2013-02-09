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

# This is currently deployment specific and not required
# with a packaged deploy (since the package is in the Python path)
BASE_DIR = os.path.join(os.path.dirname(__file__), '..')

if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from modelconvert.application import app as application

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)