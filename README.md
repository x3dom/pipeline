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



Code structure
--------------

This app is using the great flask (flask.pocoo.org) and is using the
simple file layout (no modules). You will find almost all important code
in application.py