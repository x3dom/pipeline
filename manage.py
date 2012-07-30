#!/usr/bin/env python
# manage.py
from flaskext.script import Manager

from modelconvert.application import app

manager = Manager(app)

@manager.command
def cleanup():
    print "TODO: celan orphaned files in tmp/uploads|downloads (files older than 10 minutes)"

def bootstrap():
    print("Setup local development directories")

if __name__ == "__main__":
    manager.run()
