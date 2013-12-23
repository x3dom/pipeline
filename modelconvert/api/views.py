# -*- coding: utf-8 -*-
from flask import (Blueprint, request, redirect, abort, Response, jsonify)

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
    return Response(event_stream(channel), mimetype="text/event-stream")



@api.route('/v1/bundles', methods= ['GET'])
def list_bundles():
    """
    The bundles are still hardcoded. This needs to be rectified in a future
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


@api.route('/v1/jobs', methods=['POST'])
def add_job():
    """
    Adding a job to the processing queue by accepting data. The json
    payload should look like this:

    {
        "payload": {
            "model": "model data",            // this is of course flawed for larger modles
            "model_format":"obj"
            "metadata": "metadata",           // and only for compatiblity
            "metadata_format":"xml",
            "zip": "binary zip contents"  // as long as we don't have users and persistence
            "url": "http://someurl.to/model.zip",  // alternative to the above
        },

        "email_to": "some@address.com",

        // one out of the list of names you get with /bundles
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
        // },

        // any combination of those, or no "meshlab" entry at all if
        // meshalb processing is not desired
        "meshlab": [
            "Remove Duplicate Faces",
            "Remove Duplicated Vertex",
            "Remove Zero Area Faces",
            "Remove Isolated pieces (wrt Face Num.)",
            "Remove Unreferenced Vertex",
            "Extract Information"
        ]
    }


    In return you will get a json response with various data about
    your request:

    {
        "status":{
            "code": 200,
            "message": "Job accepted with ID 123", // clear text informational message
        },

        // in case of successful handling:
        "task_id": 123,
        "job_url":   "full.host/v1/jobs/123",       // poll URI for checking less frequently for results
        "progress_url": "full.host/v1/stream/123",  // push URI for status updates
    }
    
    """
    
   if not request.json:
       return Response('', status=415, mimetype='application/json')

    options = dict() # options passted to task
    data = request.json

    if not data and not data['payload'] and not data['payload']['model'] or not data['payload']['url'] or not data['payload']['zip']:
        resp = jsonify(
            status=dict(
                code=400, 
                message="Model data not provided. Either use a URI, data from a model file, or a ZIP package."
            )
        )
        resp.status_code = 400 # bad resquest
        return resp

    if data['payload']['url']:
        # handle URL part
        pass
    else:
        # handle data in message part
        pass


    if data['payload']['email_to']:
        # we need to add at least captcha system to protect from 
        # spammers, for now setting the sender env var enables the
        # email system, use with care behind pw protected 
        if current_app.config['DEFAULT_MAIL_SENDER'] == 'noreply@localhost':
            options.update(email_to=None)
        else:
            options.update(email_to=email_to)

    if data['meshlab']:
        options.update(meshlab=data.meshlab)

    if not data['template']:
        options.update(template='basic')
    else:
        options.update(template=data.template)

    #retval = tasks.convert_model.apply_async((filename, options))
        
    #return redirect(url_for('frontend.status', task_id=retval.task_id))


@api.route('/v1/jobs/<task_id>', methods=['GET'])
def job_status(task_id):
    """ 
    Check status of a specific job.
    Note that currently this maps to a Celery Task ID. Later it will
    be a seperate entity which can have many associated celery tasks.
    
    Note that Celery returns PENDING if the Task ID is non existant.
    This is an optimization and could be recitified like so:
    http://stackoverflow.com/questions/9824172/find-out-whether-celery-task-exists

    When results are ready we provide json data response with:
    
    {   
        "status": {
            "code": 200,
            "message": "Conversion ready.",
        }
        
        "download_url":
        "preview_url:
    }
    """
    result = tasks.convert_model.AsyncResult(task_id)
    if result.ready() and result.successful():
        status_code = 200
    else:
        status_code = 102

    resp = jsonify(status=status_code, results=result.state)
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