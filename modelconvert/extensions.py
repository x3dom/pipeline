# -*- coding: utf-8 -*-


from celery import Celery

celery = Celery()

from redis import StrictRedis
red = StrictRedis()

#from flask.ext.mail import Mail
#mail = Mail()

#from flask.ext.cache import Cache
#cache = Cache()

#from flask.ext.login import LoginManager
#login_manager = LoginManager()