#!/usr/bin/env python
# manage.py
import os
import shutil
import time

from flaskext.script import Manager

from modelconvert.application import app

manager = Manager(app)
app.config.from_object('modelconvert.settings')

@manager.command
def cleanup():
    download_path = os.path.normpath(app.config["DOWNLOAD_PATH"])
    
    # simple protection against dummies. However it is questionable to
    # give them Unix rm command in this case ;)
    if not 'tmp/downloads' in download_path or download_path == '/':
        print("You are using a non-standard location for the download path.")
        print("Please create your own deletion procedure. If your fs is")
        print("mounted with mtime support, this command will work fine:\n")
        print("  find /your/path -mtime +30 -exec rm -rf '{}' \;\n")
        exit(-1)

    longevity = 6300 * 24;
    current_time = time.time();
    print("Removing files older than %i seconds" % longevity)
    
    
    for root, dirs, files in os.walk(download_path, topdown=False):
        for name in files:
            filepath = os.path.join(root, name)
            filetime = os.path.getmtime(filepath)
            if current_time - filetime > longevity:
                print("Removing file %s" % filepath)
                os.remove(filepath)
                
        for name in dirs:
            dirpath = os.path.join(root, name)
            dirtime = os.path.getmtime(dirpath)
            if current_time - dirtime > longevity:
                print("Removing directory %s" % dirpath)
                os.rmdir(dirpath)    
    
    

def bootstrap():
    print("Setup local development directories")

if __name__ == "__main__":
    manager.run()
