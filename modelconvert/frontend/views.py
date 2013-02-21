# -*- coding: utf-8 -*-
import uuid
import os
import random
import shutil
import uuid

from werkzeug import secure_filename

from flask import (Blueprint, render_template, current_app, request,
                   flash, url_for, redirect, session, abort)

from flask import jsonify
from flask import send_from_directory

from modelconvert.utils import ratelimit
from modelconvert import tasks


frontend = Blueprint('frontend', __name__)


def is_allowed_file(filename):
    """ Check if a filename has an allowed extension """
    return '.' in filename and filename.rsplit('.', 1)[1] in \
        current_app.config['ALLOWED_EXTENSIONS']


@frontend.route("/")
def home():
    """ Renders the default home page """
    return render_template('frontend/index.html')


@frontend.route("/preview")
def preview():
    """
    The URL is handled by the web-server.
    """
    pass


@frontend.route("/upload/", methods=['GET', 'POST'])
# ratelimit access to the upload function in order to prevent
# DoS and spammers. Someone who wants to bulk convert his models
# should use aopt directly.
#@ratelimit.ratelimit(limit=300, per=60 * 15)
def upload():
    """
    The upload method takes a uploaded file and puts it into
    the celery processing queue using the Redis backend. Filename
    integrity is enforced by renaming the uploaded file to a unique
    name and deleting it after successfull processing.

    """
    if request.method == 'POST':
        # FIXME: convert this to WTForms
        meshlab = request.form.getlist('meshlab')
        aopt = request.form['aopt']
        template = request.form['template']
        file = request.files['file']

        # options to pass to convertion task
        options = dict()
        

        if file and is_allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            # create a UUID like hash
            #hash = "%032x" % random.getrandbits(128)
            hash = uuid.uuid4().hex
            options.update(hash=hash)

            # anonymize filename, keep extension and save
            filename = os.path.join(current_app.config['UPLOAD_PATH'], 
                                    hash + os.path.splitext(file.filename)[1])
            file.save(filename)
            
            if meshlab:
                options.update(meshlab=meshlab)

            # in case the user uploaded a meta file, store this as well
            # FIXME make sure only processed when valid template selection
            # (DoS)
            metadata = request.files['metadata']
            if metadata:
                meta_filename = os.path.join(current_app.config['UPLOAD_PATH'], hash, 'metadata' + os.path.splitext(metadata.filename)[1])
                metadata.save(meta_filename)
                options.update(meta_filename=meta_filename)
                
            options.update(
                aopt=aopt, 
                template=template
            )

            retval = tasks.convert_model.apply_async((filename, options))
            
            return redirect(url_for('frontend.status', task_id=retval.task_id))
        else:
            flash("Please upload a file of the following type: %s" %
                ", ".join(current_app.config['ALLOWED_EXTENSIONS']), 'error')

    return render_template('frontend/index.html')





@frontend.route('/status/<task_id>/', methods=['GET'])
def status(task_id):
    """ 
    Check status of a specific job.
    
    Note that Celery returns PENDING if the Task ID is non existant.
    This is an optimization and could be recitified like so:
    http://stackoverflow.com/questions/9824172/find-out-whether-celery-task-exists
    """
    result = tasks.convert_model.AsyncResult(task_id)
    
    if request.is_xhr:
        return jsonify(state=result.state)
    else:    
        if result.ready() and result.successful():
            return redirect(url_for('frontend.success', hash=result.info['hash']))
        else:
            return render_template('frontend/status.html', result=result)


@frontend.route('/success/<hash>/', methods=['GET'])
def success(hash):
    """ 
    Display download links for converted files.
    
    Note that this also just displays simple links and does not check for
    validity if the files actually exist. This is not necessary since they
    are temporary anyway.
    """
    filenames = ['%s.html' % hash, '%s.zip' % hash]
    return render_template('frontend/success.html', hash=hash, filenames=filenames)


# This is basically redundant, Nginx or apache should handle this
# make this a wsgi middleware for development envs
@frontend.route('/download/<hash>/<filename>/', methods=['GET'])
def download(hash, filename):
    """
    Allows to download a file from the DOWNLOAD_FOLDER.
    The file is identified by a hash value and can only be
    a .zip file.

    """
#    filename = "%s.zip" % hash
    # security
    filename = os.path.basename(filename)
    
    if os.path.exists(os.path.join(current_app.config['DOWNLOAD_PATH'], hash, filename)):
        path = os.path.join(current_app.config['DOWNLOAD_PATH'], hash)
        return send_from_directory(path, filename, as_attachment=True)
    else:
        return not_found(404)



@frontend.route("/ping")
def ping():
    tasks.ping.apply_async()
    return 'pong'



# @app.route("/test")
# def hello_world():
#     """
#     Move this to a test case. This executes a predefined model conversion
#     use this for quick tests wihtout the form upload hassle
#     """
#     hash = uuid.uuid4().hex
# 
#     options = dict(hash=hash)
#     testfile = app.config["PROJECT_ROOT"] + '/tests/data/flipper.x3d'
# 
#     res = tasks.convert_model.apply_async((testfile, options))
#     context = {"id": res.task_id }
#     goto = context['id']
#     #return jsonify(goto=goto) 
#     return redirect(url_for('status', task_id=res.task_id))


# -- Celery API Rest interface -----------------------------------------------
# The URLs starting with /admin/ should be guarded by the webserver
# This is rather explict coded for better comprehnsion
# FIXME: make a JS only dashboard using the REST api below

# @app.route("/admin/")
# def admin():
#     return render_template('admin/dashboard.html')


# @app.route("/admin/tasks/registered")
# def show_registered_tasks():
#     i = celery.control.inspect()

#     if request.is_xhr:
#         return jsonify(tasks=i.registered()) 
#     else:
#         return render_template('admin/tasks/registered.html', nodelist=i.registered())


# @app.route("/admin/tasks/active/")
# def show_active_tasks():
#     i = celery.control.inspect()
#     return jsonify(tasks=i.active()) 

# @app.route("/admin/tasks/scheduled/")
# def show_scheduled_tasks():
#     i = celery.control.inspect()
#     return jsonify(tasks=i.scheduled()) 

# @app.route("/admin/tasks/waiting/")
# def show_waiting_tasks():
#     i = celery.control.inspect()
#     return jsonify(tasks=i.reserved()) 
