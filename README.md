Getting started
===============

This project follows the ususal python- and web development practices.
It deploys on the X3DOM webserver.

You never ever want to modify this on the server, use a local dev
environment to make your chanages and then deploy using the fab command.

System requirements (make sure you install them first):

 * Python 2.6
 * Redis
 * InstantReality

This applications requires a locally running redis instance.


Installing Python requirements
------------------------------

It is recommended you use virtualenv+pip for your development and
deployment enviroments. On your local development box, you should
also install fabric (pip install fabric) if you want to deploy
the code automatically.

First install requirements:

    pip install -r requirements.txt
  
Then you should be able to run the development server by issuing
the following command:

    python manage.py runserver

Point your browser to http://localhost:5000


Running all required services at once
-------------------------------------

A Procfile is provided for convenience. Use this on your local machine
to start all required services at once using foreman. 
http://ddollar.github.com/foreman/

The Procfile can also be use to deploy modelconvert to cloud services that 
support the Procfile protocol.


How to run a celery deamon on your production system
----------------------------------------------------
If you are noting using the Procfile to run the required services, you need
to configure each service on your machine (e.g. non-cloud production servers).

Redis comes as standard package with most Linux distributions. No other action
is required, short of installing the redis server package. For debian systems
this is usally done with this command:

  $ sudo apt-get install redis-server

In order to run the celery deamon on your production site, please use the
generic init script provided with celery. For more information see
http://docs.celeryproject.org/en/latest/tutorials/daemonizing.html or refer
to your devops people ;)


Code structure
--------------

This app is using the Fask microframework (flask.pocoo.org) and is using 
the module file layout. You will find almost all important code
in modelconvert/application.py

