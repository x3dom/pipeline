# -*- coding: utf-8 -*-
from flask import (Blueprint, request, redirect, abort, Response, jsonify)

from modelconvert import tasks, security

from modelconvert.extensions import red

api = Blueprint('api', __name__)


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



@api.route('/v1/bundles/', methods= ['GET'])
def list_bundles():

    # just for testing, replace with dynamic lookup    
    data = dict(
        count=2,
        next=None,
        prev=None,
        results=[
        {
            'name': 'standard',
            'display_name': 'Standard',
            'description': 'Basic standard output tempalte',
        },
        {
            'name': 'pop',
            'display_name': 'POP Geometry',
            'description': 'POP geometry template',
        }
    ])
    
    if request.headers['Content-Type'] == 'application/json':
        resp = jsonify(data)
        resp.status_code = 200
        return resp
    else:
        return Response('', status=415, mimetype='application/json')



@api.route('/v1/job/', methods=['POST'])
def process():
    pass


@api.route('/v1/job/<task_id>/', methods=['GET'])
def task_status(task_id):
    """ 
    Check status of a specific job.
    Note that currently this maps to a Celery Task ID. Later it will
    be a seperate entity which can have many associated celery tasks.
    
    Note that Celery returns PENDING if the Task ID is non existant.
    This is an optimization and could be recitified like so:
    http://stackoverflow.com/questions/9824172/find-out-whether-celery-task-exists
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