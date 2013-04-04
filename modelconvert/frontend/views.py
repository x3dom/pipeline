# -*- coding: utf-8 -*-
import uuid
import os
import random
import shutil
import uuid

import requests
import urlparse

from werkzeug import secure_filename

import flask
from flask import (Blueprint, render_template, current_app, request,
                   flash, url_for, redirect, session, abort, Response,
                   jsonify, send_from_directory)


from modelconvert import tasks, security

from modelconvert.extensions import red
from modelconvert.utils import ratelimit, humanize


frontend = Blueprint('frontend', __name__)


# TODO: cleanup pubsub business (json, events, and ids)
# FIXME: This oviously does not scale, we need to use gevent/tornado
#        or node for pub/sub services.
def event_stream(channel):
    pubsub = red.pubsub()
    pubsub.subscribe(channel)
    for message in pubsub.listen():
        yield 'retry: 3000\ndata: %s\n\n' % message['data']

@frontend.route('/stream/<channel>/')
def stream(channel):
    return flask.Response(event_stream(channel), mimetype="text/event-stream")


@frontend.route("/ping")
def ping():
    red.publish('test', 'Hello!')
    return flask.redirect('/')
    #tasks.ping.apply_async()
    #return 'pong'





@frontend.route("/")
def home():
    """ Renders the default home page """
    return render_template('frontend/index.html')


@frontend.route('/preview/<hash>/<filename>', methods=['GET'])
def preview(hash, filename):
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
        url = request.form['url']

        # options to pass to convertion task
        options = dict()

        # create a UUID like hash for temporary file storage
        #hash = "%032x" % random.getrandbits(128)
        hash = uuid.uuid4().hex
        options.update(hash=hash)



        # This whole section is kind of flimsy. 
        # - download should be performed asynchrounously, though some checks
        #   should be performed here (allowed hosts, filenames, etc.)
        # - downloading a url triggered via public web form is a HUGE security
        #   risk. Basically anyone can kill our sever by pasting a url to be
        #   downloaded. Therefore, at the  moment, the ULRs are restricted to 
        #   the ALLOWED_DOWNLOAD_HOSTS settings.

        # error handling can be done smarter
        # URL instead of file
        if url:

            # basic security
            if not security.is_allowed_host(url):
                flash("Tried to download from a insecure source ({0}). Only the following hosts are allowed: {1}".format(url, ", ".join(current_app.config['ALLOWED_DOWNLOAD_HOSTS'])), 'error')
                return render_template('frontend/index.html')

            # download file to disk
            r = requests.get(url, stream=True, verify=False)
            filename = secure_filename(os.path.split(url)[-1].split("?")[0])
            filename = os.path.join(current_app.config['UPLOAD_PATH'], filename)

            # FIXME: this should check the mimetype in the http response header
            # as well
            if not security.is_allowed_file(filename):
                flash("Please upload a file of the following type: %s" %
                ", ".join(current_app.config['ALLOWED_EXTENSIONS']), 'error')
                return render_template('frontend/index.html')

            if r.status_code == requests.codes.ok:

                if int(r.headers['content-length']) > current_app.config['MAX_CONTENT_LENGTH']:
                    flash("File too big. Please don't upload files greater than {0}".format(humanize.bytes(current_app.config['MAX_CONTENT_LENGTH'])), 'error')
                    return render_template('frontend/index.html')
                else:

                    with open(filename, "wb") as data:
                        data.write(r.content)

            else:
                flash("Could not download file {0} Status code: {1}".format(url, r.status_code), 'error')
                return render_template('frontend/index.html')

        else:
            # in case of file upload
            if file and security.is_allowed_file(file.filename):
                filename = secure_filename(file.filename)
                
                # anonymize filename, keep extension and save
                filename = os.path.join(current_app.config['UPLOAD_PATH'], 
                                        hash + os.path.splitext(file.filename)[1])
                file.save(filename)
            else:
                flash("Please upload a file of the following type: %s" %
                    ", ".join(current_app.config['ALLOWED_EXTENSIONS']), 'error')
                return render_template('frontend/index.html')


        if meshlab:
            options.update(meshlab=meshlab)

        # in case the user uploaded a meta file, store this as well
        # FIXME make sure only processed when valid template selection
        # (DoS)
        metadata = request.files['metadata']
        if metadata:
            meta_filename = os.path.join(current_app.config['UPLOAD_PATH']) + 'metadata' + os.path.splitext(metadata.filename)[1]
            metadata.save(meta_filename)
            options.update(meta_filename=meta_filename)
        
        options.update(
            aopt=aopt, 
            template=template
        )

        retval = tasks.convert_model.apply_async((filename, options))
        
        return redirect(url_for('frontend.status', task_id=retval.task_id))


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
            hash = result.info['hash']
            filenames = ['%s.html' % hash, '%s.zip' % hash]
            return render_template('frontend/status.html', result=result, hash=hash, filenames=filenames)
        #    return redirect(url_for('frontend.success', hash=result.info['hash']))
        else:
            return render_template('frontend/status.html', result=result)


# TODO: redundant now, we can delete this
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
@frontend.route('/download/<hash>/<filename>', methods=['GET'])
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
