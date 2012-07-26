# -*- coding: utf-8 -*-
import os, random
from subprocess import call

from flask import Flask, g
from flask import render_template, request, flash, session, redirect, url_for
from flask import send_from_directory

from werkzeug import secure_filename

from util.ratelimit import ratelimit

app = Flask(__name__)
app.config.from_object('settings')


def is_allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']



@app.route("/")
def home():
    return render_template('index.html')


@app.route("/upload/", methods=['GET', 'POST'])
# ratelimit access to the upload function in order to prevent
# DoS and spammers. Someone who wants to bulk convert his models
# should use aopt directly.
#@ratelimit(limit=300, per=60 * 15)
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and is_allowed_file(file.filename):
            filename = secure_filename(file.filename)

            # anonymize filename, keep extension and save
            hash = "%032x" % random.getrandbits(128)
            filename = os.path.join(app.config['UPLOAD_PATH'], hash + os.path.splitext(file.filename)[1])
            file.save(filename)
            # convert and delete original after successful conversion
            # if conversion errors out, show the relevant source portion of the
            # code
            
            # optimization under heavy load: celery + rabbitmq
            # however this is overkill at the moment and only necessary 
            # if the page load is very high.
            
            
            # assumption: contents of file matches extension
            output_filename = os.path.join(app.config['DOWNLOAD_PATH'], hash + '.html')
            status = call([app.config['AOPT_BINARY'], "-i", filename, '-N', output_filename])
            

            if status < 0:
                flash("There has been an error converting your file")
                return render_template('index.html')
                
            return redirect(url_for('download', hash=hash))
        else:
            flash("Please upload a file of the following type: %s" % \
                ",".join(app.config['ALLOWED_EXTENSIONS']), 'error')

    return render_template('index.html')

@app.route('/download/<hash>', methods=['GET'])
def download(hash):
    # check if file exists, then send it, otherwise
    # display waiting template
    filename = "%s.html" % hash
    
    if os.path.exists(os.path.join(app.config['DOWNLOAD_PATH'], filename)):
        return send_from_directory(app.config['DOWNLOAD_PATH'], filename)
    else:
        return render_template('status.html', hash=hash)






if __name__ == "__main__":
    app.run()