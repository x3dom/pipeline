# -*- coding: utf-8 -*-
import os
import random
import shutil
from contextlib import closing
from zipfile import ZipFile, ZIP_DEFLATED
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

# -- App setup --------------------------------------------------------------
# serves the static downloads in development
# in deployment apache or nginx should do that
if app.config['DEBUG']:
    from werkzeug.wsgi import SharedDataMiddleware
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
        '/preview': app.config["DOWNLOAD_PATH"]
    })


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
        aopt = request.form['aopt']
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


            output_directory = os.path.join(app.config['DOWNLOAD_PATH'], hash)
            os.mkdir(output_directory)


            if template == 'fullsize' or template == 'metadataBrowser':
                output_extension = '.x3d'
                aopt_switch = '-x'
                
                # render the template with inline
                output_template_filename = os.path.join(
                                            app.config['DOWNLOAD_PATH'], hash, 
                                            hash + '.html')

                user_tpl_env = app.create_jinja_environment()
                user_tpl = user_tpl_env.get_template(template +'/' + template + '_template.html')
                
                with open(output_template_filename, 'w+') as f:
                    f.write(user_tpl.render(X3D_INLINE_URL='%s.x3d' % hash))

                output_directory_static = os.path.join(output_directory, 'static')
                input_directory_static = os.path.join(app.config['PROJECT_ROOT'], 
                                                      'templates', template, 'static')
               
                shutil.copytree(input_directory_static, output_directory_static) 

                metadata = request.files['metadata']
                if metadata:
                    metadatafilename = os.path.join(app.config['DOWNLOAD_PATH'], hash, 'metadata' + os.path.splitext(metadata.filename)[1])
                    metadata.save(metadatafilename)       

            else:
                output_extension = '.html'
                aopt_switch = '-N'



            output_filename = hash + output_extension
            working_directory = os.getcwd()
            os.chdir(output_directory)

            if aopt == 'restuctedBinGeo':
                output_directory_binGeo = os.path.join(output_directory, "binGeo")
                os.mkdir(output_directory_binGeo)
                
                status = call([
                  app.config['AOPT_BINARY'], 
                  "-i", 
                  filename, 
                  "-u", 
                  "-b", 
                  hash + '.x3db'
                ])

                if status < 0:
                     os.chdir(working_directory)
                     flash("There has been an error converting your file", 'error')
                     return render_template('index.html')
                else:
                    status = call([
                      app.config['AOPT_BINARY'], 
                      "-i", 
                      hash + '.x3db', 
                      "-F", 
                      "Scene",
                      "-b", 
                      hash + '.x3db'
                    ])

                if status < 0:
                     os.chdir(working_directory)
                     flash("There has been an error converting your file", 'error')
                     return render_template('index.html')
                else:
                    status = call([
                      app.config['AOPT_BINARY'], 
                      "-i", 
                      hash + '.x3db', 
                      "-G", 
                      'binGeo/:saI',              
                      aopt_switch, 
                      output_filename
                    ])
                
            elif aopt == 'binGeo':
                output_directory_binGeo = os.path.join(output_directory, "binGeo")
                os.mkdir(output_directory_binGeo)
                status = call([
                  app.config['AOPT_BINARY'], 
                  "-i", 
                  filename, 
                  "-G", 
                  'binGeo/:saI', 
                  aopt_switch, 
                  output_filename
                ])


            else:  
                status = call([
                  app.config['AOPT_BINARY'], 
                  "-i", 
                  filename, 
                  aopt_switch, 
                  output_filename
                ])

   
            
            if status < 0:
                os.chdir(working_directory)
                flash("There has been an error converting your file", 'error')
                return render_template('index.html')
            else:
                zip_path = os.path.join(app.config['DOWNLOAD_PATH'], hash)
                _zipdir(zip_path, '%s.zip' % hash)
                os.chdir(working_directory)
            
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
    filenames = ['%s.html' % hash, '%s.zip' % hash]
        
    return render_template('status.html', hash=hash, filenames=filenames)



@app.route('/download/<hash>/<filename>/', methods=['GET'])
def download(hash, filename):
    """
    Allows to download a file from the DOWNLOAD_FOLDER.
    The file is identified by a hash value and can only be
    a .zip file.

    """
#    filename = "%s.zip" % hash
    # secuirty
    filename = os.path.basename(filename)
    
    if os.path.exists(os.path.join(app.config['DOWNLOAD_PATH'], hash, filename)):
        path = os.path.join(app.config['DOWNLOAD_PATH'], hash)
        return send_from_directory(path, filename, as_attachment=True)
    else:
        return not_found(404)


def _zipdir(basedir, archivename):
    assert os.path.isdir(basedir)
    with closing(ZipFile(archivename, "w", ZIP_DEFLATED)) as z:
        for root, dirs, files in os.walk(basedir):
            # ignore empty directories
            for fn in files:
                # skip self and other zip files
                if os.path.basename(fn) == os.path.basename(archivename):
                    continue
                absfn = os.path.join(root, fn)
                zfn = absfn[len(basedir)+len(os.sep):] #XXX: relative path
                z.write(absfn, zfn)


if __name__ == "__main__":
    app.run()
