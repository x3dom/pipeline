from __future__ import with_statement  # remove this as soon as sever has latest python 2.x

from fabric.api import *

# the user to use for the remote commands
env.user = 'local'
# the servers where the commands are executed
env.hosts = ['x3dom.org']

env.APP_ROOT = '/var/www/modelconvert/app'

# expects the app to be cloned once there manually
# fix this in the future and deliver a package vs. git checkout
def deploy():
    local('git push')
    with cd(env.APP_ROOT):
        run('git pull')
        run('touch wsgi.py')
