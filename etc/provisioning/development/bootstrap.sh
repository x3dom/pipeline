#!/usr/bin/env bash

# remember where we are
_CWD=`pwd`


# ----------------------------------------------------------------------
# we need recent software, so add PPAs
# ----------------------------------------------------------------------

# configure backports for automatic install
cat >/etc/apt/preferences <<EOM
Package: *
Pin: release a=precise-backports
Pin-Priority: 500
EOM

# recent postgres
cat >/etc/apt/sources.list.d/pgdg.list <<EOM
deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main
EOM

#key for postgres
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | \
  sudo apt-key add -

apt-get update
apt-get -y upgrade

# ----------------------------------------------------------------------
# basic infrastructure
# ----------------------------------------------------------------------
apt-get -y install xvfb
cat >/etc/init/xvfb.conf <<EOM
description     "Xvfb X Server"
start on (net-device-up
          and local-filesystems
          and runlevel [2345])
stop on runlevel [016]
exec /usr/bin/Xvfb :99 -screen 0 1024x768x24
EOM
service xvfb restart

apt-get -y install vim
apt-get -y install git
apt-get -y install postgresql
apt-get -y install redis-server  # old, fix this
apt-get -y install nginx         # old, fix this
apt-get -y install nodejs        # don't need yet
apt-get -y install python-setuptools
apt-get -y install python-dev
easy_install pip

# ----------------------------------------------------------------------
# instant
# ----------------------------------------------------------------------

# instant
#wget --directory=/tmp ftp://ftp.igd.fraunhofer.de/irbuild/Ubuntu-i686/InstantReality-Ubuntu-10.04-x86-2.2.0.24944.deb
#dpkg -i /tmp/InstantReality-Ubuntu-10.04-x86-2.2.0.24944.deb
#rm /tmp/InstantReality-Ubuntu-10.04-x86-2.2.0.24944.deb
# get missing dependencies from dpkg
apt-get -f install 



# ----------------------------------------------------------------------
# meshlab - we need to compile a lot of stuff here
#           this may take quite some time
# ----------------------------------------------------------------------
apt-get -y install subversion
apt-get -y install libqt4
apt-get -y install libqt4-dev qt4-dev-tools qtcreator

mkdir -p /opt/build

# TODO: check if present, if so, update instead of pull
# get meshlab from svn
if [ -d "/opt/build/meshlab/.svn" ] ; then
    cd /opt/build/meshlab/src
    svn update
else
    svn co https://meshlab.svn.sourceforge.net/svnroot/meshlab/trunk/meshlab /opt/build/meshlab
fi

if [ -d "/opt/build/vcglib/.svn" ] ; then
    cd /opt/build/vcglib
    svn update
else
    svn co https://vcg.svn.sourceforge.net/svnroot/vcg/trunk/vcglib /opt/build/vcglib
fi


cd /opt/build/meshlab/src/external
qmake -recursive external.pro 
make

cd /opt/build/meshlab/src
qmake -recursive meshlab_full.pro
make

cd $_CWD

# note we do not install meshlab anywhere but use it directly from build
# location

# ----------------------------------------------------------------------
# application setup
# ----------------------------------------------------------------------
pip install -r https://raw.github.com/x3dom/pipeline/master/requirements.txt

#
# NOTE, there's a problem when Ctrl-C ing after an error
# I don't know why but it does not terminate all celery workers
# This does not happen on OSX
#
cat >/home/vagrant/develop <<EOM
#!/bin/bash
HOME=`pwd`
cd /vagrant
exec honcho -d /vagrant -e /vagrant/etc/provisioning/development/Env -f /vagrant/etc/provisioning/development/Procfile start
cd $HOME
EOM

chmod a+x /home/vagrant/develop

# not sure if this works during setup
mkdir -p /vagrant/tmp/downloads
mkdir -p /vagrant/tmp/uploads
chown -R vagrant:vagrant /home/vagrant


# ----------------------------------------------------------------------
# cleanup
# ----------------------------------------------------------------------
# clean up
apt-get -y remove libqt4-dev qt4-dev-tools qtcreator subversion
