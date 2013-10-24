# remove this as soon as sever has latest python 2.x
from __future__ import with_statement  

import os

from fabric.api import run, cd, execute, task, sudo, local, env

# Note, this file is specific for the modelconvert.x3dom server
# Don't change this. If you want to deploy elsewhere you need
# to create your own fabfile, specific to your environment

# the user to use for the remote commands
env.user = 'localadmin'

# the servers where the commands are executed
env.hosts = ['pipeline.v-must.net']

env.APP_ROOT = '/home/localadmin/app/pipeline'


# expects the app to be cloned once there manually
# fix this in the future and deliver a package vs. git checkout
@task
def deploy():
    """
    Deploys the code on the production server
    """
#    local('git push')
    with cd(env.APP_ROOT):
        run('git fetch origin; git reset --hard origin/master')
#        run('python -c "import compileall; compileall.compile_dir(\'.\')"')
        run('touch modelconvert/wsgi.py')
        run('circusctl restart webapp')

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


# this is probalby better suited in manage.py, however since
# app templates are going to be outsourced, i put it here
@task
def update_x3dom():
    local("curl http://www.x3dom.org/download/dev/x3dom-full.js -o modelconvert/bundles/_shared/static/x3dom-full.js")
    local("curl http://www.x3dom.org/download/dev/x3dom.css -o modelconvert/bundles/_shared/static/x3dom.css")
    local("curl http://www.x3dom.org/download/dev/x3dom.js -o modelconvert/bundles/_shared/static/x3dom.js")
    local("curl http://www.x3dom.org/download/dev/x3dom.swf -o modelconvert/bundles/_shared/static/x3dom.swf")


@task
def clean():
    local("rm -rf modelconvert.egg-info")

