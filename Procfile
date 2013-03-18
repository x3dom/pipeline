# this procfile is for development only and simplifies launching of required
# services. Please use this in development only. 
# Youc an use honcho (python) or foreman (ruby):
# https://github.com/nickstenning/honcho
# http://ddollar.github.com/foreman/

redis: redis-server etc/init/redis.conf
celery: python manage.py celeryworker
web: python manage.py runserver --threaded