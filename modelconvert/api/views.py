# -*- coding: utf-8 -*-
from flask import (Blueprint, request, redirect, abort, Response)

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


@api.route("/ping")
def ping():
    red.publish('test', 'Hello!')
    return redirect('/')
    #tasks.ping.apply_async()
    #return 'pong'

