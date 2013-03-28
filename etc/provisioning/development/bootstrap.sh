#!/usr/bin/env bash

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

# xvfb
apt-get install -y xvfb
cat >/etc/init/xvfb.conf <<EOM
description     "Xvfb X Server"
start on (net-device-up
          and local-filesystems
          and runlevel [2345])
stop on runlevel [016]
exec /usr/bin/Xvfb :99 -screen 0 1024x768x24
EOM
service xvfb restart

# basic infrastructure
apt-get install -y vim
apt-get install -y git
apt-get install -y postgresql
apt-get install -y redis-server
apt-get install -y nginx
apt-get install -y nodejs
apt-get install -y python-setuptools
apt-get install -y python-dev
easy_install pip

# instant
#wget --directory=/tmp ftp://ftp.igd.fraunhofer.de/irbuild/Ubuntu-i686/InstantReality-Ubuntu-10.04-x86-2.2.0.24944.deb
#dpkg -i /tmp/InstantReality-Ubuntu-10.04-x86-2.2.0.24944.deb
#rm /tmp/InstantReality-Ubuntu-10.04-x86-2.2.0.24944.deb
# get missing dependencies from dpkg
apt-get -f install 

# meshlab - we need to compile a lot of stuff here
# install re prereqs
# download meshlab from repo
# build
# install


# application setup
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
