import os, sys
# fix this with packaged deploy
sys.path.insert(0, '/var/www/modelconvert/apps/modelconvert')
from application import app as application

from barrel import cooper
logins = [('x3dom', 'x3dom')]


application = cooper.formauth(users=logins)(application)