import os
import sys

# fix this with packaged deploy
sys.path.insert(0, '/var/www/modelconvert/modelconvert')
from modelconvert.application import app as application
