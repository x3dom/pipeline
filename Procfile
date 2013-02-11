# this procfile is for development only
# install foreman to use this
redis: redis-server /usr/local/etc/redis.conf
#celery: celery --app=modelconvert.tasks.celery worker -l info
celery: python manage.py celery
web: python manage.py runserver
