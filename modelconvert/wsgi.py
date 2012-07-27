import os
import sys

# fix this with packaged deploy
sys.path.insert(0, '/var/www/modelconvert/apps/modelconvert')
from modelconvert.application import app as application
