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

This project works in a Python ecosystem. Therefore you need to install
some libraries, and in rare cases Python, on you system. 

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
probalby in luck. Python is a core component of most Linux systems. In 
order to verify your Python version type the following command in wyour
shell:

.. code-block:: bash
    
    $ python --version 
  

If the version is smaller than 2.6 you need to upgrade your 10 year old
installation of Python. Even if your package manager does not provide a 
more recent version, rolling your own is quite simple. The `Python`_
website provides you with all relevant information or prepared packages
for your OS.

We have not tested this application on Windows. The development enviornment
may be working there too, but it not supported. If you have to use
Windows, `VirtualBox`_ is your friend and `Vagrant`_ might make it even
simpler.



----------------
Python Libraries
----------------

Python is equipped with a libarary package manager you can use to
install required libraries (easy_install). However, we recommend using
a more modern package management solution called `pip`_. In order to
seperate the libararies from your system, so you can use different
versions for different projects, we recommend using `virtualenv`_ for 
your development and deployment enviroments. 

Those are no strict requirements and just make life easier, if you want
to proceed without pip/virtualenv you need to manage your libararies
manually. In this manual we assume at least PIP to follow along.

First, install pip:

.. code-block:: bash

    $ sudo easy_install pip
  

Then install modelconvert requirements:

.. code-block:: bash

    $ pip install -r requirements.txt
  

Then you should be able to run the development server by issuing
the following command:

.. code-block:: bash

    $ python manage.py runserver


Point your browser to http://localhost:5000. The Application will not work
properly at this point, but the home page should be rendered. Press 
Ctrl-C to exit for now.



--------------
InstantReality
--------------

Since we are dealing with experimental features, you should always use a
recent `nightly build`_.

The modelconvert service is currently tested on Ubuntu Lucid32, and 
Mac OS X 10.6.8.



-------------
Meshlabserver
-------------

You can get Meshlab from http://www.meshlab.org/. Installation depends
on your system. 



-----
Redis
-----

We recommend to use a recent 2.x version of redis. The ones distributed
with Linux distributions are usually out of date. Compiling redis is 
simple. Please follow instructions on the `Redis`_ website.


===============
Getting started
===============

This app is using the `Flask_` microframework with Blueprints. Program entry
point is ``core.py`` which configures the application. You will find 
almost all important code in ``frontend/views.py`` and ``tasks.py``.

The modelconvert application must be configured in order to run properly. It
ships with sensible defaults, but usually you need to configure it for
production. Especially paths to ``aopt`` and ``meshlabserver`` as well as a 
session key need to be set. There are bascially two ways to accomplish this.

  * Configuring the application by setting environment variables
  * Creating config file which overrides/sets values

Configuration through OS environment variables is the preferred way to 
configure the modelconvert application. If you use `Honcho`_ or Procfile in
development, this can be done by creating a ``.env`` file in the root checkout.
For example:

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

In server environments, there are many ways to do this: Webserver config, 
startup script, wsgi file, virtualenv loaders, etc. **Note**: the env 
variables also must be set when running the celery worker daemon. 
Make sure that debugging is turned off in your production configuration.

Additionally or alternatively you can set a environment variable on your 
system which points to a config file that overrides the default values or the
values you set through individual environment variables. Just set the 
``MODELCONVERT_SETTINGS`` variable to point to your config
file like so:

.. code-block:: bash

    $ export MODELCONVERT_SETTINGS=/path/to/yoursettings.py

Of course this can also be done in the ``.env`` file. Alternatively, just 
create a small shell script:

.. code-block:: bash

    $ echo '#!/bin/sh\nexport=MODELCONVERT_SETTINGS=/path/to/settings.py\nhoncho start' >> manage.sh
    $ chmod a+x run.sh
    $ ./manage.sh



-----------------------
Configuration Variables
-----------------------

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



------
Flower
------

There's an nice tool called `Flower`_ to graphically manage and monitor 
the celery task queue. We highly recommend it for debugging purposes on the 
production system. It has been installed with the requirement.txt loading 
business above. So you should be ready to go. Please refer to the `Flower`_
manual for more information.

  

=======================
Development Enviornment
=======================

A `Procfile`_ is provided for convenience. You can use this on your local 
machine to start all required services at once using `Honcho`_.

.. code-block:: bash
    
    $ honcho start

This runs all the services in the background and concacts the output in one
log stream. The Procfile can also be use to deploy modelconvert to cloud 
services that support the Procfile protocol.

If you do not want to use `Honcho`_ in development, no problem, you need to 
start the services manually on seperate terminals or in screen/tmux sessions.




==========
Deployment
==========

--------------------------------
Provisioning a production system
--------------------------------
In order to deploy the application in a prodcution environment, you need to
provision your deployment machine accordingly. We are currently working on
a set of `Puppet`_ manifests to do that automatically - for the time being,
you need to do the work manually. The steps outline here are tested on Ubuntu
10.4 LTS (lucid32), but should be similar on other distributions.

~~~~~
Redis
~~~~~

Redis comes as standard package with most Linux distributions. No other action
is required, short of installing the redis server package. For Debian systems
this is usally done with apt:

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

The `Redis`_ website provides you with more detailed information.

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
