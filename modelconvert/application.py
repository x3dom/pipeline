# -*- coding: utf-8 -*-
import os
import random
from subprocess import call

from flask import Flask, g
from flask import render_template, request, flash, session, redirect, url_for
from flask import send_from_directory
from werkzeug import secure_filename

# used for user template
from jinja2 import Template

from utils.ratelimit import ratelimit

app = Flask(__name__)
app.config.from_object('modelconvert.settings')


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


def is_allowed_file(filename):
    """ Check if a filename has an allowed extension """
    return '.' in filename and filename.rsplit('.', 1)[1] in \
        app.config['ALLOWED_EXTENSIONS']


@app.route("/")
def home():
    """ Renders the default home page """
    return render_template('index.html')


@app.route("/upload/", methods=['GET', 'POST'])
# ratelimit access to the upload function in order to prevent
# DoS and spammers. Someone who wants to bulk convert his models
# should use aopt directly.
#@ratelimit(limit=300, per=60 * 15)
def upload():
    """
    The upload method takes a uploaded file and puts it into
    the celery processing queue using the Redis backend. Filename
    integrity is enforced by renaming the uploaded file to a unique
    name and deleting it after successfull processing.

    """
    if request.method == 'POST':
        template = request.form['template']
        file = request.files['file']
        if file and is_allowed_file(file.filename):
            filename = secure_filename(file.filename)

            # anonymize filename, keep extension and save
            hash = "%032x" % random.getrandbits(128)
            filename = os.path.join(app.config['UPLOAD_PATH'], 
                                    hash + os.path.splitext(file.filename)[1])
            file.save(filename)
            
            
            ##
            # THE FOLLOWING CODE SHOULD RUN IN A CELERY TASK
            ##
            # convert and delete original after successful conversion
            # if conversion errors out, show the relevant source             
            # portion of the code
            
            # optimization under heavy load: celery + redis
            # however this is overkill at the moment and only necessary 
            # if the page load is very high.
            
            
            # assumption: contents of file matches extension
            
            # straight forward and simplistic way of selecting a template 
            # and generating inline style output
            if template == 'ios':
                output_extension = '.x3d'
                aopt_switch = '-x'
                
                # render the template with inline
                output_template_filename = os.path.join(
                                            app.config['DOWNLOAD_PATH'], 
                                            hash + '.html')

                user_tpl_env = app.create_jinja_environment()
                user_tpl = user_tpl_env.get_template('vmust_ipad_template.html')
                
                with open(output_template_filename, 'w+') as f:
                    f.write(user_tpl.render(X3D_INLINE_URL='%s.x3d' % hash))

            else:
                output_extension = '.html'
                aopt_switch = '-N'
                
            output_filename = os.path.join(app.config['DOWNLOAD_PATH'], 
                                           hash + output_extension)
            status = call([
                app.config['AOPT_BINARY'], 
                "-i", 
                filename, 
                aopt_switch, 
                output_filename
            ])
            
            if status < 0:
                flash("There has been an error converting your file", 'error')
                return render_template('index.html')
            else:
                pass
            
            if not app.config['DEBUG']:
                # delete the uploaded file
                os.remove(filename)
            ##
            # END CELERY TASK
            ##

            return redirect(url_for('status', hash=hash))
        else:
            flash("Please upload a file of the following type: %s" %
                ", ".join(app.config['ALLOWED_EXTENSIONS']), 'error')

    return render_template('index.html')


def queue():
    """ Show the processing queue """
    pass


@app.route('/status/<hash>/', methods=['GET'])
def status(hash):
    """ Check status of a specific job, display download link when ready """

    filenames = ['%s.html' % hash]
    if os.path.exists(os.path.join(app.config['DOWNLOAD_PATH'], "%s.x3d" % hash)):
        # we know it's an inlined conversion
        filenames = ['%s.html' % hash, '%s.x3d' % hash]
        
    return render_template('status.html', filenames=filenames)


@app.route('/download/<filename>/', methods=['GET'])
def download(filename):
    """
    Allows to download a file from the DOWNLOAD_FOLDER.
    The file is identified by a hash value and can only be
    a .html file.

    """
#    filename = "%s.html" % hash
    # secuirty
    filename = os.path.basename(filename)
    
    if os.path.exists(os.path.join(app.config['DOWNLOAD_PATH'], filename)):
        return send_from_directory(app.config['DOWNLOAD_PATH'], filename, as_attachment=True)
    else:
        return not_found(404)


if __name__ == "__main__":
    app.run()