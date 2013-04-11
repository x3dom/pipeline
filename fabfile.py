# remove this as soon as sever has latest python 2.x
from __future__ import with_statement  

import os

from fabric.api import *

# Note, this file is specific for the modelconvert.x3dom server
# Don't change this. If you want to deploy elsewhere you need
# to create your own fabfile, specific to your environment

# the user to use for the remote commands
env.user = 'local'


# the servers where the commands are executed
env.hosts = ['x3dom.org']

env.APP_ROOT = '/var/www/modelconvert/modelconvert'


def hub():
    env.APP_ROOT = '/home/localadmin/app/modelconvert'
    env.hosts = ['hub.igd.fraunhofer.org']


# expects the app to be cloned once there manually
# fix this in the future and deliver a package vs. git checkout
@task
def deploy():
    """
    Deploys the code on the production server (x3dom.org)
    """
#    local('git push')
    with cd(env.APP_ROOT):
        run('git fetch origin; git reset --hard origin/master')
#        run('python -c "import compileall; compileall.compile_dir(\'.\')"')
        run('touch wsgi.py')
        sudo('/etc/init.d/apache2 restart', pty=False)
        sudo('supervisorctl restart celery', pty=False)


@task
def bootstrap():
    """
    Try to bootstrap a development environment. Requires fabric, pip.
    """
    local('python manage.py mkdirs')
    local("pip install -r requirements.txt")

    # download meshlab for the platform we are on and put it to tmp/meshlab
    # download latest IR for the platform and put it into tmp/ir

    # if osx:
    #     cd meshlab && ln -s Contents/MacOS bin
    #     cd ir && ln -s Contents/MacOS bin
    # conveniece

    # print instructions for installing redis
    # create a settings-dev.py and print instruction of how to use it
    # export MODELCONVERT_SETTINGS='/path/to/settings-dev.py'   

@task
def clean():
    local("rm -rf modelconvert.egg-info")


@task
def mkvm():
    """
    Try to provision a VM (req. VirtualBox, Vagrant)
    """
    print "Nothing here yet, move along"
