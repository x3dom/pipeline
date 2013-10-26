********************************
3D model optimization for humans
********************************

Modelconvert is an experimental 3D model optimization and
sharing service. It allows optimization and conversion 
of 3D models for Web presentation and sharing these
models on the web.

.. image:: https://github.com/x3dom/pipeline/raw/master/docs/_images/modelconvert.jpg
    :alt: Modelconvert Screenshots


Modelconvert is written in Python, and under the hood it uses the excellent
`Flask`_ and `Celery`_ libraries as well as `Meshlab`_ and `InstantReality`_

Check out the official `docs`_ for more (still in progress).

.. image:: https://secure.travis-ci.org/x3dom/pipeline.png
    :target: https://travis-ci.org/x3dom/pipeline


**Table of Contents**

.. contents::
    :local:
    :depth: 2
    :backlinks: none


=============
Main Features
=============

* Upload and conversion of 3D Models to X3DOM
* Sharing of models on the web (permalinks to converted models)
* Downloadable ZIP packages of converted models
* Triangular Mesh optimization of models
* Converted/Optimized models can be embedded in different templates
* Asynchronous process
* Server-Sent Events for fast status updates
* Upload archives with many models and textures at once

And soon:

* Personalized upload manager for multiple uploads in one view
* Come back later and reprocess models with different settings without
  uploading again
* Manage your models and what you share with whom
* User uploadable templates
* Much more


============
Installation
============

This project works in a Python ecosystem and depends on two external software 
solutions: `InstantReality`_ and `Meshlab`_. Therefore you need to install
those packages first, and in rare cases a recent Python, on your system. 

System requirements:
 
 * `Python`_ 2.7 (2.6 works too)
 * `Redis`_
 * `InstantReality`_
 * `Meshlab`_
 * On Unix/Linux a xvfb framebuffer or a running X11 instance


--------------------------------------------------------
The quick and easy path (if everything works as planned)
--------------------------------------------------------
We provide a method of boostrapping a complete development environment in a
virtual machine. This is done using four different open source tools you need 
to install first on your system:

  * `VirtualBox`_, a virtualization software 
  * `Vagrant`_ , a virtualization software manager
  * `Git`_, a source control system to get the code
  * a SSH client in your PATH (on Unix systems this is usually installed, Windows users: `PuTTY`_)

After installing these components on your system you need to drop to the
command line and issue the following commands. Make sure you have a 
live internet connection, since this process downloads a lot of stuff:

.. code-block::
    
    $ git clone https://github.com/x3dom/pipeline.git modelconvert
    $ cd modelconvert                
    $ vagrant up
    $ vagrant ssh
    $ ./develop                                                     

This sequence of commands downloads the code from GitHub, provisions a 
virtual machine with all the software you need to develop with the
system, then SSHs into machine and launches the development server.

Next, point your browser to: http://localhost:5001

With a bit of luck, you'll have a working virtual machine with everything
installed and running. You can edit code on your local machine - the
virtual machine autmatically mounted the folder on your host machine.

To stop working on the project it is important to suspend the virtual 
machine instead of not shutting down. This is required in order to skip
the provisioning step when you resume:

.. code-block::
    
    $ <Ctr-C>^
    $ logout                  (or Ctr-D)       
    $ vagrant suspend         <- back on local machine

Then when you come back to work on the project again:

.. code-block:: bash
    
    $ vagrant resume
    $ vagrant ssh
    $ ./develop               <- runs on the vm

If provisioning code changed, you need to reload the virtual machine with
this command:

.. code-block:: bash
    
    $ vagrant reload

In order to destory the machine and start over, issue:

.. code-block:: bash
    
    $ vagrant destroy

Read more about this in the `Vagrant`_ documentation.


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

The steps outlined here are tested on Ubuntu 10.04 LTS (lucid32), but should be 
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

You get a fresh nightly here: http://www.instantreality.org/downloads/dailybuild/

NB: at the moment, the Ubuntu 12.04 builds have temporary upload problems.
Meanwhile you can grab the builds from here: http://www.x3dom.org/temp/IR/

The modelconvert service is currently tested on Ubuntu Lucid32, and 
Mac OS X 10.6. We are only using the aopt tool from the Instant Reality 
package. This tool can be found in the ``bin`` directory of the Linux build and
in the ``Contents/MacOS`` directory of the Mac Application.

Unless it's not already in the PATH (you can check this by issuing 
``which aopt``), note down the absolute path to the ``aopt`` binary, you'll 
need it later.


--------------
Meshlab Server
--------------

The Meshlab Server version used inside the CIF pipeline is a special version of the Meshlab Server released
with Meshlab. Binaries or installers are not released for this version, hence you need to compile it 
from the scratch. To do so, you have to follow the instructions at:

http://sourceforge.net/apps/mediawiki/meshlab/index.php?title=Compiling

for what concern to get the source code and to resolve the external dependencies.

Regarding the compilation we report below the instructions distinguishing between using or not the Qt Creator.

*Compiling without the Qt Creator*

The compiling step depends on the compiling environment. Using GCC (both under linux and using the mingw gcc provided with 
the free Qt distribution) you should just type, from the meshlab/src directory:

.. code-block:: bash
    
    $ qmake -recursive meshlabserver_vmust.pro
    $ make

This compile the Meshlab Server and all the plugins needed to work into the CIF pipeline.

**Compiling with the Qt Creator**

In order to easily compile the external libraries and MeshLab using the Qt Creator IDE we suggest to go around the 
shadow-build system introduced by Qt Creator.

    - Import the ``.pro`` file ( File->Open File or Project... )
    - Click on Finish button in the Project setup form
    - Click on the Projects Icon in the Left Bar on Qt Creator Main Window
    - Both for Debug and Release setup change "Build directory" parameter on:
        
        - MESHLAB_DIR/src/external for external.pro project
        - MESHLAB_DIR/src for meshlabserver_vmust.pro 


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

You can use a `Procfile`_ to manage services during development. This is an easy
way to start all required services at once on your local machine. In order
to use this mechanism, copy the file ``<project>/share/Procfile.example`` 
into ``<project>/Procfile`` and adapt to match your system. For example, 
if your Redis server is not already running you need to uncomment and/or 
adapt the respective line in your ``Procfile``. The Procfile is not checked 
into the repository, since each development environment is different.

When done, use `Honcho`_ (which has been installed with the requirements) to 
launch the Procfile.

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
``modelconvert/tasks/``.

The modelconvert application must be configured in order to run properly. It
ships with sensible defaults for development, but you need to configure it for
production. If you have ``aopt`` and ``meshlabserver`` in your PATH, youre
set for development. However it is sensibel to set some basic values.

The application is configured through operating system environment variables. 
If you use `Honcho`_ or Foreman in development, the environment can easily be 
set by creating a ``.env`` file in the root checkout. For example:

.. code-block:: bash

    $ cat >.env <<EOM
    DEBUG="True"
    DEVELOPMENT_MODE="True"
    MESHLAB_BINARY="/path/to/meshlabserver"
    AOPT_BINARY="/path/to/aopt"
    MESHLAB_DISPLAY=":0"
    ADMINS="admin@somedomain.com"
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

    $ export MODELCONVERT_SETTINGS="/path/to/yoursettings.py"

Of course, this can also be done in the ``.env`` file.

Alternatively, just create a small shell script:

.. code-block:: bash

    $ echo '#!/bin/sh\nMODELCONVERT_SETTINGS="/path/to/config.py" python manage.py run' >> manage.sh
    $ chmod a+x manage.sh
    $ ./manage.sh


.. warning:: Be sure you don't have leading or trailing whitespaces in the 
             environment variable values. To be certain, use quotes around
             the values.


~~~~~~~~~~~~~~~~~~~~~~~
Configuration Variables
~~~~~~~~~~~~~~~~~~~~~~~

The following configuration variables can be set from the environemnt.
For more variables which can be overridden with a external config file, 
see the `settings.py`_ file.


======================  =======================================================
Variable                Description
======================  =======================================================
SECRET_KEY              For session generation. You absolutely need to 
                        set this in production environments. To generate
                        a key run python on the command line and type this:

                        >>> import os
                        >>> os.urandom(24)

                        There is a default, but please only use this
                        in development.

ADMINS                  A comma seperated list of Email addresses. This
                        is used to send notification emails to the 
                        app maintainers.
                        default: root@localhost

DEBUG                   Enable/disable debug mode.
                        default: False (possible: False, True)

DOWNLOAD_PATH           Absolute path to directory that is used to
                        store generated files. The directory needs to
                        be writable by the process which owns the 
                        application. It needs to be readable by the
                        webserver. You should override the default
                        value in production.
                        default: <module_dir>/../tmp/downloads

UPLOAD_PATH             Absolute path to directory which holds uploaded
                        files. This needs to be read/writable by the
                        application process. You should override the
                        default value in production.
                        default: <module_dir>/../tmp/uploads

AOPT_BINARY             Absolute path to the aopt binary (including
                        executable). default: aopt (PATH lookup)

MESHLAB_BINARY          Absolute path to the meshlabserver binary 
                        (including the executable). 
                        default: meshlabserver (PATH lookup)

MESHLAB_DISPLAY         X11 display port for meshlabserver. Set this to
                        you default display in a non headless setup. For
                        a headless setup the default is :99, you need
                        to run a Xvfb instance there.
                        default: ':99'

ALLOWED_DOWNLOAD_HOSTS  A list of hosts which are allowed to download
                        files from. Basic secuirty for the "download model
                        from URL functionality". You need to set this with
                        the environment through a comma seperated list e.g.:
                        x3dom.modelconvert.org,someother.domain.com
                        default: localhost:5000


CELERY_BROKER_URL       Celery broker url
                        default: redis://localhost:6379/0

SERVER_NAME             The name and port number of the server. 
                        Required for subdomain support (e.g.: 'myapp.dev:5000') 
                        Note that localhost does not support subdomains 
                        so setting this to "localhost" does not help. 
                        Setting a SERVER_NAME also by default enables 
                        URL generation without a request context but 
                        with an application context.
                        default: none

DEFAULT_MAIL_SENDER     Email address From field for outgoing emails. This 
                        setting also controls wether the mail features is active
                        or not. You need to change the default to another value
                        in order to acticate it. This is a temporary security measure.
                        default: noreply@localhost

MAIL_SERVER             The SMTP server, default: localhost
MAIL_PORT               The STMP port, default: 25
MAIL_USE_TLS            Use TLS auth, default: False
MAIL_USE_SSL            Use SSL auth, default: False
MAIL_USERNAME           Mailserver username, default: "" (empty)
MAIL_PASSWORD           Mailserver password, default: "" (empty)


MAX_CONTENT_LENGTH      File upload limit in bytes. Caution: the default is very
                        loose. If a POST or PUT request exeeds this limit
                        a http 413 is returned. Tweak this to your needs but 
                        be aware that POST/PUT bombs are a common attack vector.
                        default 134217728 (128MB)

TEMPLATE_PATH           Where the UI templates reside. 
                        default: module_dir/templates

STATIC_PATH             Where the static assets for the UI reside. 
                        default: module_dir/static

BUNDLES_PATH            Where the user templates reside. Usually you 
                        don't want to override this.
                        default: module_dir/bundles
                   
LOGFILE                 Absolute path to a file to pipe stdout logging 
                        to. This should not be used in production. 
                        default: False (stdout logging)

DEVELOPMENT_MODE        Enable/disable dev mode. This is a old setting
                        and will be removed. Set to false in production.
                        default: False (possible: False, True)
======================  =======================================================

~~~~~~~~~~~~~~~
Other variables
~~~~~~~~~~~~~~~
The following variables can only be set through the system environment.

=================   ===========================================================
Variable            Description
=================   ===========================================================
OSG_LOG_LEVEL       Set the OpenSG log level (aopt/opensg). Values: FATAL, 
                    WARNING, NOTICE, INFO, DEBUG
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
   DEBUG mode. However you need to restart if you make changes to ``tasks/*.py``.







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

============
Contributing
============

Developing patches should follow this workflow:

    1. Fork on GitHub (click Fork button)
    2. Clone to computer: ``git clone git@github.com:«github account»/x3dom/pipeline.git modelconvert``
    3. cd into your repo: ``cd x3dom``
    4. Set up remote upstream: ``git remote add -f upstream git://github.com/x3dom/pipeline.git``
    5. Create a branch for the new feature: ``git checkout -b my_new_feature``
    6. Work on your feature, add and commit as usual

Creating a branch is not strictly necessary, but it makes it easy to delete 
your branch when the feature has been merged into upstream, diff your branch 
with the version that actually ended in upstream, and to submit pull requests 
for multiple features (branches).

    7.  Push branch to GitHub: ``git push origin my_new_feature``
    8.  Issue pull request: Click Pull Request button on GitHub


**Useful Commands**

If a lot of changes has happened upstream you can replay your local changes 
on top of these, this is done with ``rebase``, e.g.:

.. code-block:: bash

    git fetch upstream
    git rebase upstream/master


This will fetch changes and re-apply your commits on top of these.

This is generally better than merge, as it will give a clear picture of which 
commits are local to your branch. It will also “prune” any of your local 
commits if the same changes have been applied upstream.

You can use ``-i`` with ``rebase`` for an “interactive” rebase. This allows you 
to drop, re-arrange, merge, and reword commits, e.g.:

.. code-block:: bash

    git rebase -i upstream/master



============
Publications
============
The following publications describe this system further:

* A. Aderhold, Y. Jung, K. Wilkosinska, D. Fellner, "Distributed 3D model 
  optimization for the Web with the Common Implementation Framework for 
  Online Virutal Museums" in *Proceedings Digital Hertiage 
  Conference 2013*, t.b.p.

* K. Wilkosinska, A. Aderhold, H. Graf, and Y. Jung, "Towards a common 
  implementation framework for online virtual museums" in *Proceedings HCI 
  International 2013:* DUXU, Part II, ser. LNCS, A. Marcus, Ed., 
  vol. 8013. Heidelberg: Springer, 2013, pp. 321–330. 
  `Online. <http://link.springer.com/chapter/10.1007%2F978-3-642-39241-2_36>`_


================
Acknowledgements
================

Portions of the this work was carried out in the project v-must, which has received 
funding from the European Community's Seventh Framework Programme (FP7 2007/2013) 
under grant agreement 270404.

Icons by `Glyphish`_


.. _Flask: http://flask.pocoo.org
.. _docs: http://pipeline.rtfd.org
.. _Celery: http://celeryproject.org
.. _Meshlab: http://meshlab.sourceforge.net
.. _InstantReality: http://instantreality.org
.. _virtualenv: http://www.virtualenv.org/en/latest/
.. _virtualenvwrapper: http://www.doughellmann.com/projects/virtualenvwrapper/
.. _pip: http://pypi.python.org/pypi/pip
.. _Python: http://python.org
.. _Redis: http://redis.io
.. _PuTTY: http://www.putty.org/
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
.. _Glyphish: http://glyphish.com
.. _settings.py: https://github.com/x3dom/pipeline/blob/master/modelconvert/settings.py
