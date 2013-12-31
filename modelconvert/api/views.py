# -*- coding: utf-8 -*-
import uuid
import os
import tempfile
import urlparse

import werkzeug
import requests

from flask import (Blueprint, request, redirect, abort, Response, jsonify, current_app, url_for)

from modelconvert import tasks, security

from modelconvert.extensions import red

api = Blueprint('api', __name__)



@api.route('/v1', methods= ['GET'])
def api_info():
    """
    Get basic API meta information
    """
    data = dict(
        version=1,
        base_url=request.url,
        help="http://pipeline.readthedocs.org/en/latest/api.html"
    )
    resp = jsonify(data)
    return resp


# TODO: cleanup pubsub business (json, events, and ids)
# FIXME: This oviously does not scale, we need to use gevent/tornado
#        or node for pub/sub services.
def event_stream(channel):
    pubsub = red.pubsub()
    pubsub.subscribe(channel)
    for message in pubsub.listen():
        yield 'retry: 3000\ndata: %s\n\n' % message['data']


@api.route('/v1/stream/<channel>/')
def stream(channel):
    """
    Push EventSource formatted messages to the client. This can be used
    to display real-time status information.
    """
    return Response(event_stream(channel), mimetype="text/event-stream")



@api.route('/v1/bundles', methods= ['GET'])
def list_bundles():
    """
    The bundles are still hardcoded at this time. This needs to be rectified in a future
    version when bundles are self contained python modules which are dynamically
    loaded.
    """

    data = dict(
        count=8,
        next=None,
        prev=None,
        bundles=[
        {
            'name': 'basic',
            'display_name': 'Basic',
            'description': 'Basic viewer application',
        },
        {
            'name': 'standard',
            'display_name': 'Standard',
            'description': 'Standard viewer application',
        },
        {
            'name': 'cadViewer',
            'display_name': 'CAD Viewer',
            'description': 'CAD Viewer application',
        },
        {
            'name': 'fullsize',
            'display_name': 'Fullsize',
            'description': 'Fullsize viewer',
        },
        {
            'name': 'metadata',
            'display_name': 'Metadata',
            'description': 'Metadata viewer',
        },
        {
            'name': 'pop',
            'display_name': 'POP Geometry',
            'description': 'POP geometry template',
        },
        {
            'name': 'radianceScaling',
            'display_name': 'Radiance Scaling',
            'description': 'Radiance Scaling viewer',
        },
        {
            'name': 'walkthrough',
            'display_name': 'Walkthrough',
            'description': 'Walkthrough viewer',
        },
    ])

    resp = jsonify(data)
    return resp
    
    # only used for put/post
    # if request.json:
    #     pass
    # else:
    #     return Response('', status=415, mimetype='application/json')


@api.route('/v1/buckets', methods=['POST'])
def add_bucket():
    """
    This methods allows for uploading arbitrary files to the server
    which later are used for processing::

        POST /buckets

    The HTTP request requires a filename header to identify the file::

        X-Filename: herkules.ply

    Additionally the Content-Type header needs to be set to::

        Content-Type: application/octet-stream

    You can then stream binary content in the body.

    Note that you have to specify a filename even if you stream the 
    file directly from an application. This is required in case you
    want to upload other assets to the bucket which are name dependent
    (for exmaple when using the metadata template).

    After successful upload, a bucket ID among with a status message and
    the filename under which the data is stored within he bucket.
    """
    
    # create a UUID like hash for temporary file storage (bucket id)
    hash = uuid.uuid4().hex

    if not request.headers['Content-Type'] == 'application/octet-stream':
        resp = jsonify(message="Unsupported media type. Maybe you forgot to set X-Filename header?")
        resp.status_code = 415 # bad resquest
        return resp

    if not 'X-Filename' in request.headers:
        resp = jsonify(message="You probalby forgot to set X-Filename header?")
        resp.status_code = 415 # bad resquest
        return resp

    if not request.data:
        resp = jsonify(message="Please support data with your request?")
        resp.status_code = 415 # bad resquest
        return resp

    filename = request.headers['X-Filename']
        
    if security.is_allowed_file(filename):
        filename = werkzeug.secure_filename(filename)
        ofilename = filename
        upload_directory = os.path.join(current_app.config['UPLOAD_PATH'], hash)
        os.mkdir(upload_directory)
        filename = os.path.join(upload_directory, filename)

        try:
            with open(filename, "wb") as data:
                data.write(request.data)

            resp = jsonify(
                message="Payload dropped sucessfully",
                bucket_id=hash,
                filename=ofilename,
            )
            resp.status_code = 201 # created
            return resp
        except IOError:
            current_app.logger.error("Can not save {0}. Abort.".format(filename))
            resp = jsonify(message="Problem saving uploaded file")
            resp.status_code = 500 # server error
            return resp

    else:
        resp = jsonify(message="Filename unsecure, upload rejected.")
        resp.status_code = 420 # policy not fullfilled
        return resp




@api.route('/v1/buckets/<bucket_id>', methods=['POST'])
def add_to_bucket(bucket_id=None):
    """
    Not implemented yet.

    Additionally with the use of this id it is possible to upload 
    multiple files to the same bucket sequentially. e.g.::

        POST /buckets/id123

    This feature is not yet implemented. For the moment, if you like
    to upload multiple files to the same bucket, please use a ZIP file.

    """
    resp = jsonify(message="This functionality is not implemented yet. Please upload a ZIP file with all files you need.")
    resp.status_code = 501 # not impl.
    return resp
    


@api.route('/v1/jobs', methods=['POST'])
def add_job():
    """
    Adding a job to the processing queue either by fetching data from
    a known source or by using a previously created bucket full off
    resources (see ..)::

        {
            "payload": "bucket://1234afdsafdsfdsa232", 

            // for the moment you also need to specify the filename you want 
            "payload_filename: "herkules.ply"
            
            // alternatively, to load from a URI use this instead:
            "payload": "http://someplace.zip", 

            // all the following are optional:
            "email_to": "some@address.com",

            // array of strings representing meshlab filters. leave out
            // "meshlab" entry at all if no meshalb pre-processing is desired
            "meshlab": [
                "Remove Duplicate Faces",
                "Remove Duplicated Vertex",
                "Remove Zero Area Faces",
                "Remove Isolated pieces (wrt Face Num.)",
                "Remove Unreferenced Vertex",
                "Extract Information"
            ]

            // one out of the list of names you get with /bundles
            // always use the "name" field you get from GET /bundles as the name
            // might change. You can cache the names locally but be sure to expire
            // once in a while.
            "template": "basic",

            // the bundle name to be used for this job
            // in the future its also possible to override templte specific settings and options (shown but noop)
            //"bundle": {
            //    "name": "modelconvert.bundles.pop",   // this can also contain a bundle spec and related data
            //    "settings": {
            //        "aopt.pop": true,
            //        "aopt.command": "{command} {input} {output} -what -ever={0} -is -required",
            //        "meshlab.enabled": false,
            //   }
            // }
        }

    For exmaple a simple payload to convert a single model without meshalb
    sourced from a URL could look like this::

        {
            "payload": "http://domain.tld/model.obj",
            "template": "basic"
        }

    In return you will get a json response with various data about
    your request::

        {
            // clear text informational message, HTTP status code serves as numeric indicator
            "message": "Job accepted with ID 123", 

            // the task ID the job is running on
            "task_id": "123",

            // poll URI for checking less frequently for results
            "job_url":   "full.host/v1/jobs/123",       

            // URI for status updates through push protocl. This implements
            // the W3C EventSource specification. So your client needs to
            // support this in order to reciece push updates.
            "progress_url": "full.host/v1/stream/123",  
        }
    """
    
    options = dict() # options passted to task
    data = request.json

    if not data or not 'payload' in data:
        resp = jsonify(message="No payload provided. You need to specify what to convert.")
        resp.status_code = 400 # bad resquest
        return resp


    url = urlparse.urlparse(data['payload'])
    current_app.logger.info("Found {0} payload".format(url.scheme))

    if url.scheme == 'http':
        #
        #  FIXME BIGTIME
        #  THE URL DOWNLOADING SHOULD OCCUR IN THE TASK AND NOT BLOCK
        #  THE INTERFACE
        #
        if not security.is_allowed_host(data['payload']):
            resp = jsonify(message="Tried to download from a insecure source ({0}). Only the following hosts are allowed: {1}".format(url.netloc, ", ".join(current_app.config['ALLOWED_DOWNLOAD_HOSTS'])))
            resp.status_code = 403 #forbidden
            return resp

        # download file to disk
        r = requests.get(data['payload'], stream=True, verify=False)
        filename = werkzeug.secure_filename(os.path.split(data['payload'])[-1].split("?")[0])

        # FIXME: this should check the mimetype in the http response header
        # as well
        if not security.is_allowed_file(filename):
            resp = jsonify(message="Please upload a file of the following type: %s" %
            ", ".join(current_app.config['ALLOWED_EXTENSIONS']))
            resp.status_code = 403 #forbidden
            return resp


        if r.status_code == requests.codes.ok:

            if int(r.headers['content-length']) > current_app.config['MAX_CONTENT_LENGTH']:
                resp = jsonify(message="File too big. Please don't try to use files greater than {0}".format(humanize.bytes(current_app.config['MAX_CONTENT_LENGTH'])))
                resp.status_code = 416 # request range unsatifieable
                return resp
            else:
                
                # create a UUID like hash for temporary file storage
                hash = uuid.uuid4().hex

                upload_directory = os.path.join(current_app.config['UPLOAD_PATH'], hash)
                os.mkdir(upload_directory)
                filename = os.path.join(upload_directory, filename)

                with open(filename, "wb") as data:
                    data.write(r.content)

                options.update(hash=hash)
        else:
            resp = jsonify(message="Could not download file {0} Status code: {1}".format(data['payload'], r.status_code))
            resp.status_code = 416 # request range unsatifieable
            return resp


    elif url.scheme == 'bucket':

        if not 'payload_filename' in data:
            resp = jsonify(message="Please specify the payload_filename attribute in your request.")
            resp.status_code = 400 # bad
            return resp

        filename = data['payload_filename']  #refactor this
        current_app.logger.debug("Using Bucket ID: {0} with entry point filename".format(url.netloc, filename))
        options.update(hash=url.netloc)
    else:
        current_app.logger.error("Unknown payload resource identifier")
        resp = jsonify(message="No recognizable payload URI provided. Please use bucket:// or http://")
        resp.status_code = 400 # bad resquest
        return resp

    
    if 'email_to' in data['payload']:
        # we need to add at least captcha system to protect from 
        # spammers, for now setting the sender env var enables the
        # email system, use with care behind pw protected 
        if current_app.config['DEFAULT_MAIL_SENDER'] == 'noreply@localhost':
            options.update(email_to=None)
        else:
            options.update(email_to=email_to)

    if 'meshalb' in data:
        options.update(meshlab=data.meshlab)

    if not 'template' in data:
        options.update(template='basic')
    else:
        options.update(template=data.template)

  

    retval = tasks.convert_model.apply_async((filename, options))
    
    resp = jsonify(
        message="Task added sucessfully.",
        task_id=retval.task_id,
        job_url=url_for('.job_status', _external=True, task_id=retval.task_id),
        progress_url=url_for('.stream', _external=True, channel=retval.task_id)
    )
    resp.status_code = 201 # created
    return resp



@api.route('/v1/jobs/<task_id>', methods=['GET'])
def job_status(task_id):
    """ 
    Check status of a specific job.
    Note that currently this maps to a Celery Task ID. Later it will
    be a seperate entity which can have many associated celery tasks.
    
    Note that Celery returns PENDING if the Task ID is non existant.
    This is an optimization and could be recitified like so:
    http://stackoverflow.com/questions/9824172/find-out-whether-celery-task-exists

    When results are ready we provide json data response with::
    
        {   
            "message": "Conversion ready.",
            "download_url":"http:/domain.tld/somplace/download.zip",
            "preview_url": "htt://domain.tld/someplace/index.html",
        }
    """
    result = tasks.convert_model.AsyncResult(task_id)

    if result.failed():
        current_app.logger.error("Conversion failed. {0}".format(result.info))
        resp = jsonify(
            message="Conversion failed. {0}".format(result.info),
            state=result.state,
        )
        status_code = 500

    elif result.ready() and result.successful():
        filenames = result.info['filenames']
        hash = result.info['hash']
        resp = jsonify(
            message="Conversion Ready.",
            state=result.state,
            download_url=url_for('frontend.download', _external=True, hash=hash, filename=filenames[1]),
            preview_url =url_for('frontend.preview', _external=True, hash=hash, filename=filenames[0])
        )
        status_code = 200

    else:
        resp = jsonify(
            message="Conversion in progress",
            state=result.state,
            progress_url=url_for('.stream', _external=True, channel=task_id)
        )
        status_code = 102

    resp.status_code = status_code

    return resp




# @api.route("/ping")
# def ping():
#     red.publish('test', 'Hello!')
#     return redirect('/')
#     #tasks.ping.apply_async()
#     #return 'pong'


# @api.route('/v1/echo', methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
# def api_echo():
#     if request.method == 'GET':
#         return "ECHO: GET\n"

#     elif request.method == 'POST':
#         return "ECHO: POST\n"

#     elif request.method == 'PATCH':
#         return "ECHO: PACTH\n"

#     elif request.method == 'PUT':
#         return "ECHO: PUT\n"

#     elif request.method == 'DELETE':
#         return "ECHO: DELETE"