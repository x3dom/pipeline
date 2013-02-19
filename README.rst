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

The modelconvert application can (and probably must) be configured in 
in order to run properly. Especially paths to aopt and meshlab need
to be set in the ``settings.py`` file. The settings file however should not
be changed in the canonical repository. There are several ways to accomplish 
this without changing the ``settings.py`` file directly.

  * Forking the project on `GitHub`_ and makeing changes on your fork. 
  * If you are a core developer, the changes can be made on a seperate 
    branch (or otherwise prevented from being pushed back to github)
  * Setting a environmet variable with a config file

You can set a environment variable on your system which points
to a config file that overrides the values in settings.py. Just
set the ``MODELCONVERT_SETTINGS`` variable to point to your config
file like so:

.. code-block:: bash

    $ export MODELCONVERT_SETTINGS=/path/to/yoursettings.py

In order to set this whenever you run the manage script, just create
a small shell script:

.. code-block:: bash

    $ echo '#!/bin/sh\nexport=MODELCONVERT_SETTINGS=/path/to/settings.py\nforeman start' >> run.sh
    $ chmod a+x run.sh
    $ ./run.sh

In production environments, you should also set this variable, in the WSGI file
for exmaple, and point it to a configuration valid for the deployment. Make 
sure that debugging is turned off in your production configuration.

For the moment, please use the forking or branching and modify settings.py
directly. The config from envvar is not yet fully realized.


---------------------
Temporary directories
---------------------
Befire you begin, you also need to create temporary directories as specified 
in ``settings.py`` or, more likely, your own ``settings.py`` file.


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
machine to start all required services at once using `Foreman`_.

.. code-block:: bash
    
    $ foreman start

This runs all the services in the background and concacts the output in one
log stream. The Procfile can also be use to deploy modelconvert to cloud 
services that support the Procfile protocol.

If you do not want to use `Foreman`_ in development, no problem, you need to 
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
.. _Foreman: http://ddollar.github.com/foreman/
.. _daemonizing: http://docs.celeryproject.org/en/latest/tutorials/daemonizing.html
.. _xvfb: http://en.wikipedia.org/wiki/Xvfb
.. _Flower: https://github.com/mher/flower
.. _mod_wsgi: http://code.google.com/p/modwsgi/
.. _nginx: http://nginx.org/
.. _uwsgi: http://wiki.nginx.org/HttpUwsgiModule
