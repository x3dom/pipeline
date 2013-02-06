Getting started
===============

This project works in a Python web app ecosystem and follows good generic
web development practices. It deploys on the X3DOM webserver. If you want to
deploy on another server. You need to modify some files in your fork of this
project.

You never ever want to modify files on your server directly, use a local dev
environment to make your chanages and then deploy using the fab command.

System requirements (make sure you install them first):
 
 * Python 2.7 (2.6 works too)
 * Redis
 * InstantReality
 * Meshlabserver
 * xvfb X11 framebuffer (headless) or
 * Running X11 instance


Installing Python
------------------
If you are running Linux or another Unix distro, you are in luck. Python
is a core component of most systems. Type:

  $ python --version 
  
To see what version you are on. If it is smaller than 2.6 you need to upgrade.
Even if your package manager does not provide a more recent version, rolling
your own if quite simple. Check out www.python.org.

We have not tested this application on windows. The development enviornment
may be working there too, but it not supported. If you have to use
Windows, VirtualBox is your friend (helper: vagrantup.com)


Installing Python requirements
------------------------------
We recommende to use virtualenv+pip for your development and
deployment enviroments. 

  http://www.virtualenv.org/en/latest/
  http://www.doughellmann.com/projects/virtualenvwrapper/
  http://pypi.python.org/pypi/pip

Although it is not a strict requirement, at least PIP should be installed. Or
otherwise you need to install all packages listed in requirements.txt 
manually.

On your local development box, you should also install fabric (pip install fabric) if you want to deploy the code automatically to the x3dom server.

First, install requirements:

    pip install -r requirements.txt
  
Then you should be able to run the development server by issuing
the following command:

    python manage.py runserver

Point your browser to http://localhost:5000. The Application will not work
properly at this point, but the home page should be rendered. So press 
Ctrl-C to exit.


Installing Instant Reality
--------------------------
Since we are dealing with experimental features, you should always use a
recent nightly build from here:

  http://www.instantreality.org/downloads/dailybuild/
  
The modelconvert service is currently tested on Ubuntu Lucid32, and 
Mac OS X 10.6.8.


Installing Meshlabserver
------------------------
You can get Meshlab from here http://www.meshlab.org/. Installation depends
on your system. 


Installing redis
----------------
We recommend to use a recent version of redis. The ones distributed
with Linux distributions are usually out of date (except Arch maybe). 
Compiling redis is simple. Please follow instructions here:

  http://redis.io/



Configuration
-------------
Please modify the settings.py file to adapt to your systems. In order to
achieve this smoothly, we recommend you fork the project on GitHub and make
the changes on your fork. If you are a core developer, the changes should
be made on a seperate branch (or otherwise prevented from being pushed back
to github)



Running all required services at once during development
--------------------------------------------------------
A Procfile is provided for convenience. You can use this on your local machine
to start all required services at once using foreman  (http://ddollar.github.com/foreman/):

  $ foreman start

This runs all the services in the background and concacts the output in one
log stream. The Procfile can also be use to deploy modelconvert to cloud 
services that support the Procfile protocol, like Heroku.

If you don't want to use foreman in development, you need to start the
services manually on seperate terminals or in screen/tmux sessions.


How to run the required deamons on your production system
---------------------------------------------------------
If you are noting using the Procfile to run the required services, you need
to configure each service on your server machine.

Redis comes as standard package with most Linux distributions. No other action
is required, short of installing the redis server package. For debian systems
this is usally done with this command:

  $ sudo apt-get install redis-server

In order to run the celery deamon on your production site, please use the
generic init/upstart script provided with celery. For more information see
http://docs.celeryproject.org/en/latest/tutorials/daemonizing.html or refer
to your devops people ;)

In order to use meshlab, you also need a running X11 instance or xvfb on 
DISPLAY :99 if you are running a headless setup (the display number can be
changed in the settings file). Plese refer to your Linux distribution of
how to setup xvfb (http://en.wikipedia.org/wiki/Xvfb)

Flower
######
There's an nice tool called Flower to graphically manage the celery
task queue. We highly recommend it for debugging purposes on the production
system. 

  https://github.com/mher/flower


Web Server Deployment
---------------------
Depending on your system, you can deploy using Apache mod_wsgi for 
convenience. The more sensible option however is nginx/uwsgi. More detailed
info on how to deploy can be found here:

  http://flask.pocoo.org/docs/deploying/


Code structure
--------------
This app is using the Fask microframework (flask.pocoo.org) and is using 
the module file layout. You will find almost all important code
in modelconvert/application.py and tasks.py.

At first, you also need to create temporary directories as specified in 
settings.py.


