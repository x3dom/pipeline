#!/usr/bin/env python
from __future__ import absolute_import

import os
import shutil
import time
import datetime

from flask.ext.script import Manager

from modelconvert.utils import fs
from modelconvert import create_app


app = create_app()

manager = Manager(app)
app.config.from_object('modelconvert.settings')
app.config.from_envvar('MODELCONVERT_SETTINGS', silent=True)

# serves the static downloads in development
# in deployment apache or nginx should do that
if app.config['DEBUG']:
    from werkzeug.wsgi import SharedDataMiddleware
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
        '/preview': app.config["DOWNLOAD_PATH"]
    })


@manager.command
def run():
    app.run()


@manager.command
def celeryworker():
    """
    Runs celery worker within the Flask app context
    """
    from modelconvert.tasks import celery
    import sys
    with app.app_context():
        celery.worker_main(['worker', '-E', '-l', 'INFO'])

#
# FIXME: move this to a celerybeats task
#
@manager.command
def cleanup():
    """
    Removes generated files older than 
    """
    download_path = os.path.abspath(app.config["DOWNLOAD_PATH"])
    
    # simple protection against dummies. However it is questionable to
    # give them Unix rm command in this case ;)
    if not 'tmp/downloads' in download_path or download_path == '/':
        print("You are using a non-standard location for the download path.")
        print("Please create your own deletion procedure. If your fs is")
        print("mounted with mtime support, this command will work fine:\n")
        print("  find /your/path -mtime +30 -exec rm -rf '{}' \;\n")
        exit(-1)

    longevity = 6300 * 24
    current_time = time.time();
    print("Removing files older than {0}".format(datetime.timedelta(seconds=longevity)))
    
    
    for root, dirs, files in os.walk(download_path, topdown=False):
        for name in files:
            filepath = os.path.join(root, name)
            filetime = os.path.getmtime(filepath)
            if current_time - filetime > longevity:
                print("Removing file %s" % filepath)
                os.remove(filepath)
                
        for name in dirs:
            dirpath = os.path.join(root, name)
            #dirtime = os.path.getmtime(dirpath)
            #if current_time - dirtime > longevity:
            if not os.listdir(dirpath):
                print("Removing directory %s" % dirpath)
                os.rmdir(dirpath)    


@manager.command
def mkdirs():
    """
    Create required directories from settings
    """

    dirs = [
        app.config['UPLOAD_PATH'],
        app.config['DOWNLOAD_PATH'],
    ]

    for directory in dirs:
        directory = os.path.abspath(directory)
        print("Creating directory {0}".format(directory))
        fs.mkdir_p(directory)



if __name__ == "__main__":
    manager.run()
