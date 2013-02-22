********************************
3D model optimization for humans
********************************

Modelconvert is a experimental 3D model optimization service.
It allows optimization and conversion of 3D models for Web 
presentation.

.. image:: https://github.com/x3dom/pipeline/raw/master/design/modelconvert.jpg
    :alt: Modelconvert Screenshots


Modelconvert is written in Python, and under the hood it uses the excellent
`Flask`_ and `Celery`_ libraries as well as `Meshlab`_ and `InstantReality`_


.. image:: https://secure.travis-ci.org/x3dom/pipeline.png


**Table of Contents**

.. contents::
    :local:
    :depth: 2
    :backlinks: none


=============
Main Features
=============

* Upload and conversion of 3D Models to X3DOM
* Triangular Mesh optimization of models
* Converted/Optimized models can be embedded in tempaltes
* Asynchronous process



============
Installation
============

This project works in a Python ecosystem and depends on two external software 
solutions: `InstantReality`_ and `Meshlab`_. Therefore you need to install
those packages first, and in rare cases a recent Python, on your system. 

System requirements (make sure you install them first):
 
 * `Python`_ 2.7 (2.6 works too)
 * `Redis`_
 * `InstantReality`_
 * `Meshlab`_
 * On Unix/Linux a xvfb framebuffer or a running X11 instance


------
Python
------

If you are running a Linux distribution or any variant of Unix, you are 
probalby in luck. Python is a core component of most Unix systems and part
of the LSB. In order to verify your Python version type the following command 
in your shell:

.. code-block:: bash
    
    $ python --version 
  

If the version is smaller than 2.6 you need to upgrade your installation of 
Python to a more recent one. Even if your package manager does not provide a 
more recent version, rolling your own is quite simple. The `Python`_
website provides you with all relevant information or prepared packages
for your OS.

Python is equipped with a libarary package manager you can use to
install required libraries (easy_install). However, we recommend using
a more modern package management solution called `pip`_. The following
instructions expect you have installed pip as well. If that's not the case you
can quickly install pip with the follwing command:

.. code-block:: bash
    
    $ sudo easy_install pip
  
In order to seperate the libararies from your system install, we recommend 
using `virtualenv`_ and `virtualenvwrapper`_ for your development and 
deployment enviroments. Virtualenv also installs pip for you. If you are not 
using virtualenv, and not acting as root user, you probably need to prefix the 
pip command in the following instructions with ``sudo``.

.. note:: Please do not use your systems package manager (e.g. apt, yum, pacman) to 
   install Python libraries. Always use pip.

The steps outline here are tested on Ubuntu 10.4 LTS (lucid32), but should be 
similar on other distributions.

We have not tested this application on Windows. The development enviornment
may be working, but no guarantees. If you have to use Windows, `VirtualBox`_ 
is your friend and `Vagrant`_ might make it even simpler.


--------------
InstantReality
--------------

Since we are dealing with experimental features, you should always download a
recent `nightly build`_ and install with:

.. code-block:: bash
    
    $ sudo dpkg -i <downloaded-file.deb>

The modelconvert service is currently tested on Ubuntu Lucid32, and 
Mac OS X 10.6. We are only using the aopt tool from the Instant Reality 
package. This tool can be found in the ``bin`` directory of the Linux build and
in the ``Contents/MacOS`` directory of the Mac Application.

Unless it's not already in the PATH (you can check this by issuing 
``which aopt``), note down the absolute path to the ``aopt`` binary, you'll 
need it later.


-------------
Meshlabserver
-------------

You can get Meshlab from http://www.meshlab.org/. Installation depends
on your system. You need the path to the ``meshlabserver`` binary.

Unless it's not already in the PATH, note down the absolute path to the 
``meshlabserver`` binary, you'll need it later.


--------
X Server
--------

In order to use meshlab, you also need a running X11 instance or `xvfb`_ on 
DISPLAY number 99 if you are running a headless setup (the display number 
can be overridden by the app configuration). Plese refer to your Linux 
distribution of how to setup `xvfb`_.

On Mac OS X there's no need to setup xvfb nor to start X.


-----
Redis
-----

Redis is a key-value database comes as standard package with most Linux 
distributions. No other action is required, short of installing the redis 
server package. For Debian systems this is usally done with apt:

.. code-block:: bash
    
    $ sudo apt-get install redis-server

However, there's a catch. You need a fairly recent version of Redis (2.x).
Ubuntu/Debian 10.4 does not provide that by default. In order to get this
you need to add the Dotdeb repositories to your APT sources. Create a new list
file in /etc/apt/sources.list.d/ with the following content:

.. code-block:: bash

    # /etc/apt/sources.list.d/dotdeb.org.list
    deb http://packages.dotdeb.org squeeze all
    deb-src http://packages.dotdeb.org squeeze all

Then you need to authenticate these repositories using their public key.

.. code-block:: bash

    $ wget -q -O - http://www.dotdeb.org/dotdeb.gpg | sudo apt-key add -


And finally, update your APT cache and install Redis.

.. code-block:: bash

    $ sudo apt-get update
    $ sudo apt-get install redis-server


It's also very easy to compile Redis on your own, in case you have a compiler
installed on your production system (which you probably should not have).

We recommend to use a recent 2.x version of redis. The ones distributed
with Linux distributions are usually out of date. Compiling redis is 
simple. Please follow instructions on the `Redis`_ website.

In the development environment it's not necessary to start the redis server 
on your system by default.


---
Git
---
You need the distributed version controll system Git. Check if you have it 
installed already, otherwise install it:

.. code-block:: bash

   $ which git
   $ sudo apt-get install git-core



===============
Getting started
===============


--------------------
Getting modelconvert
--------------------
First, clone the modelconvert repository from github:

.. code-block:: bash

   $ git clone https://github.com/x3dom/pipeline.git modelconvert

You now have a directory ``modelconvert`` which contains the whole 
application, change dir into it.


-----------------------------
Installing required libraries
-----------------------------

.. note:: If you are using virtualenv/wrapper, activate your virtualenv now.


Install modelconvert requirements with pip:

.. code-block:: bash

    $ pip install -r requirements.txt





---------
Launching
---------

Modelconvert uses a `Procfile`_ to manage services during development. You can 
use this on your local machine to start all required services at once 
using `Honcho`_ (which has been installed with the requirements). If your 
Redis server is alreadu running you need to uncomment the respective line
in the ``Procfile``.

.. code-block:: bash
    
    $ honcho start

This runs all the services in the background and concacts the output in one
log stream. The Procfile can also be use to deploy modelconvert to cloud 
services that support the Procfile protocol.

If you do not want to use `Honcho`_ in development, no problem, you need to 
start the services manually on seperate terminals or in screen/tmux sessions.
Just inspect the Procfile for what to start.

Point your browser to http://localhost:5000. The Application will **not** work
properly at this point, but the home page should be rendered. Press 
Ctrl-C to exit for now.




-------------
Configuration
-------------

This app is using the `Flask`_ microframework with Blueprints. Program entry
point is ``modelconvert/core.py`` which configures the application. You will 
find almost all relevant code in ``modelconvert/frontend/views.py`` and 
``modelconvert/tasks.py``.

The modelconvert application must be configured in order to run properly. It
ships with sensible defaults for development, but you need to configure it for
production. If you have ``aopt`` and ``meshlabserver`` in your PATH, youre
set for development. However it is sensibel to set some basic values.

The application is configured through operating system environment variables. 
If you use `Honcho`_ or Foreman in development, the environment can easily be 
set by creating a ``.env`` file in the root checkout. For example:

.. code-block:: bash

    $ cat >.env <<EOM
    DEBUG=True
    DEVELOPMENT_MODE=True
    MESHLAB_BINARY=/path/to/meshlabserver
    AOPT_BINARY=/path/to/aopt
    MESHLAB_DISPLAY=:0
    ADMINS=admin@somedomain.com
    EOM

When launching the development environment like so:

.. code-block:: bash

    $ honcho start

The variables contained in the ``.env`` file are automatically set.


Additionally or alternatively you can set a environment variable on your 
system which points to a config file that overrides the default values or the
values you set through individual environment variables. Just set the 
``MODELCONVERT_SETTINGS`` variable to point to your config
file like so:

.. code-block:: bash

    $ export MODELCONVERT_SETTINGS=/path/to/yoursettings.py

Of course, this can also be done in the ``.env`` file.

Alternatively, just create a small shell script:

.. code-block:: bash

    $ echo '#!/bin/sh\nMODELCONVERT_SETTINGS=/path/to/config.py python manage.py run' >> manage.sh
    $ chmod a+x manage.sh
    $ ./manage.sh




~~~~~~~~~~~~~~~~~~~~~~~
Configuration Variables
~~~~~~~~~~~~~~~~~~~~~~~

The following configuration variables can be set from the environemnt.
For more variables which can be overridden with a external config file, 
see the `settings.py`_ file.


=================   ===========================================================
Variable            Description
=================   ===========================================================
SECRET_KEY          For session generation. You absolutely need to 
                    set this in production environments. To generate
                    a key run python on the command line and type this:

                    >>> import os
                    >>> os.urandom(24)

                    There is a default, but please only use this
                    in development.

DEBUG               Enable/disable debug mode.
                    default: False (possible: False, True)

DOWNLOAD_PATH       Absolute path to directory that is used to
                    store generated files. The directory needs to
                    be writable by the process which owns the 
                    application. It needs to be readable by the
                    webserver. You should override the default
                    value in production.
                    default: <module_dir>/../tmp/downloads

UPLOAD_PATH         Absolute path to directory which holds uploaded
                    files. This needs to be read/writable by the
                    application process. You should override the
                    default value in production.
                    default: <module_dir>/../tmp/uploads

AOPT_BINARY         Absolute path to the aopt binary (including
                    executable). default: aopt (PATH lookup)

MESHLAB_BINARY      Absolute path to the meshlabserver binary 
                    (including the executable). 
                    default: meshlabserver (PATH lookup)

MESHLAB_DISPLAY     X11 display port for meshlabserver. Set this to
                    you default display in a non headless setup. For
                    a headless setup the default is :99, you need
                    to run a Xvfb instance there.
                    default: ':99'

CELERY_BROKER_URL   Celery broker url
                    default: redis://localhost:6379/0

SERVER_NAME         The name and port number of the server. 
                    Required for subdomain support (e.g.: 'myapp.dev:5000') 
                    Note that localhost does not support subdomains 
                    so setting this to "localhost" does not help. 
                    Setting a SERVER_NAME also by default enables 
                    URL generation without a request context but 
                    with an application context.
                    default: none

TEMPLATE_PATH       Where the user templates reside. Usually you 
                    don't want to override this.
                    default: module_dir/templates/bundles
                    
LOGFILE             Absolute path to a file to pipe stdout logging 
                    to. This should not be used in production. 
                    default: False (stdout logging)

DEVELOPMENT_MODE    Enable/disable dev mode. This is a old setting
                    and will be removed. Set to false in production.
                    default: False (possible: False, True)
=================   ===========================================================



---------------------
Temporary directories
---------------------

Before you begin developing, you can automatically create temporary directories 
as specified per your settings:

.. code-block:: bash

    $ python manage.py mkdirs



-------
Finally
-------

You are now ready to develop. Start the services:

.. code-block:: bash

    $ honcho start

And point your browser to ``http://localhost:5000``. To shut down 
press ``Ctrl-C``.


.. note:: Usually you do not need to restart honcho when you make changes in 
   DEBUG mode. However you need to restart if you make changes to ``tasks.py``.







==========
Deployment
==========

-- Work in progress --


-----------------
App Configuration
-----------------

In production environments, you need to configure the application through
environment variables as well. There are many ways to do this: Webserver config, 
startup script, wsgi file, virtualenv loaders, etc. 

.. note:: The env variables also must be set when running the celery worker daemon. 
   Make sure that debugging is turned off in your production configuration.



--------------------------------
Provisioning a production system
--------------------------------

In order to deploy the application in a prodcution environment, you need to
provision your deployment machine accordingly. There are severals ways to do
this automatically with tools like `Puppet`_ or Chef. You can of course do this
manually as well. 


~~~~~~
Celery
~~~~~~

In order to run the `Celery`_ deamon on your production site, please use the
generic init/upstart script provided with celery. For more information see
the `daemonizing`_  chapter of the Celery documentation or refer to your 
devops people ;)

~~~~
Xvfb
~~~~

In order to use meshlab, you also need a running X11 instance or `xvfb`_ as 
DISPLAY number 99 if you are running a headless setup (the display number 
can be overridden in you config file). Plese refer to your Linux distribution 
of how to setup `xvfb`_.

~~~~~~~~~
Webserver
~~~~~~~~~

Depending on your system, you can deploy using Apache `mod_wsgi`_ for 
convenience. The more sensible option however is `nginx`_/`uwsgi`_. More detailed
info on how to deploy can be found here:

    `http://flask.pocoo.org/docs/deploying/ <http://flask.pocoo.org/docs/deploying/>`_



~~~~~~
Flower
~~~~~~

There's an nice tool called `Flower`_ to graphically manage and monitor 
the celery task queue. We highly recommend it for debugging purposes on the 
production system. It has been installed with the requirement.txt loading 
business above. So you should be ready to go. Please refer to the `Flower`_
manual for more information.



================
Acknowledgements
================

The described work was carried out in the project v-must, which has received 
funding from the European Community's Seventh Framework Programme (FP7 2007/2013) 
under grant agreement 270404.



.. _Flask: http://flask.pocoo.org
.. _Celery: http://celeryproject.org
.. _Meshlab: http://meshlab.sourceforge.net
.. _InstantReality: http://instantreality.org
.. _virtualenv: http://www.virtualenv.org/en/latest/
.. _virtualenvwrapper: http://www.doughellmann.com/projects/virtualenvwrapper/
.. _pip: http://pypi.python.org/pypi/pip
.. _Python: http://python.org
.. _Redis: http://redis.io
.. _Virtualbox: https://www.virtualbox.org/
.. _Vagrant: http://vagrantup.com
.. _nightly build: http://www.instantreality.org/downloads/dailybuild/
.. _GitHub: http://github.com/x3dom/pipeline
.. _Procfile: https://devcenter.heroku.com/articles/procfile
.. _Honcho: https://github.com/nickstenning/honcho/
.. _daemonizing: http://docs.celeryproject.org/en/latest/tutorials/daemonizing.html
.. _xvfb: http://en.wikipedia.org/wiki/Xvfb
.. _Flower: https://github.com/mher/flower
.. _mod_wsgi: http://code.google.com/p/modwsgi/
.. _nginx: http://nginx.org/
.. _uwsgi: http://wiki.nginx.org/HttpUwsgiModule
.. _Puppet: https://puppetlabs.com/
.. _settings.py: https://github.com/x3dom/pipeline/blob/master/modelconvert/settings.py
