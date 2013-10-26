.. _deployment:


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
