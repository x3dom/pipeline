# remove this as soon as sever has latest python 2.x
from __future__ import with_statement  

from fabric.api import *

# Note, this file is specific for the modelconvert.x3dom server
# Don't change this. If you want to deploy elsewhere you need
# to create your own fabfile, specific to your environment

# the user to use for the remote commands
env.user = 'local'


# the servers where the commands are executed
env.hosts = ['x3dom.org']

env.APP_ROOT = '/var/www/modelconvert/modelconvert'

# expects the app to be cloned once there manually
# fix this in the future and deliver a package vs. git checkout
@task
def deploy():
    """
    Deploys the code on the production server (x3dom.org)
    """
#    local('git push')
    with cd(env.APP_ROOT):
        run('git pull')
#        run('python -c "import compileall; compileall.compile_dir(\'.\')"')
        run('touch wsgi.py')
        sudo('/etc/init.d/apache2 restart', pty=False)
        sudo('supervisorctl restart celery', pty=False)


@task
def mktempdirs():
    """
    Create default temporary directories.
    """
    print "Nothing here yet, move along"


@task
def mkvm():
    """
    Try to provision a VM (req. VirtualBox, Vagrant)
    """
    print "Nothing here yet, move along"

