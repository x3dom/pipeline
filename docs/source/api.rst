.. _api:


========
REST API
========

The pipeline can be driven using a restful API through the HTTP protocol.
It is therefore possible to use the advanced distributed queing system as well
as the application assembling functionality through 3rd party applications or
for batch processing.

The API follows an Restful archtictural approach and makes advanced 
use of HTTP verbs and JSON data structures.

In the following documentation the resource URIs are realtive to the 
service endpoint::

    http://localhost:5000/api/v1

Localhost is used throughout this exmaple and refers to a development
environment. Just replace the host/port part of the domain with your
network installation.

------
Basics
------
To acceess the API you need to send a properly encoded HTTP request to the 
service endpoint. The encoding of the request neesd to be UTF-8 and the 
mimetype needs to be set to ``application/json``. You can use the cURL tool
to test your requests, e.g::

    curl -H "Content-type: application/json" -X GET \
        http://localhost:5000/api/v1/bundles

~~~~~~~~~
Resources
~~~~~~~~~
In a RESTful pardigm each URL represents a unique resource. Requests are
safe, idempotent, and cacheable. Through the use of HTTP verbs certain actions
can be expressed using HTTP protocol means, instead of defining a new and 
arbitrary vocabulary for operations on resources.  While most browsers today 
only implement GET and POST verbs, this is not a limiting factor for APIs.
For example, in order to delete a resource, the HTTP DELETE verb is used on a 
uinque resource URI.


~~~~~
Json 
~~~~~
TODO




--------
Overview
--------

===========   =========================    ==============     ======================================================
 HTTP verb     URI                          Return codes       Description
===========   =========================    ==============     ======================================================
GET            /bundles                     200                Returns a JSON formatted list of application bundles
GET            /jobs/<task-id>              200, 102           Returns status of a job with given GUID. Will return 
                                                               HTTP status code 102 if the job can't be found or is 
                                                               still processing.
                                                               Returns a 200 if job did complete.
                                                               You can make a HEAD request without sending
                                                               data to make the lookup quicker.
                                                               If the job did complete, JSON response includes
                                                               details.
                                                               It is probably best to not query the backend
                                                               too often (maybe every 5 seconds).
GET            /jobs                        200,404            Returns a list of jobs, 404 if no jobs are found
POST           /jobs                        200,               Add a new job to the queuing system. By default
                                                               processing starts immediately.
GET            /stream/<task-id>/                              Live updates of processing events. This endpoint
                                                               provides a push service with EventSource type 
                                                               messages. It can be used to display realtime status
                                                               messages.
===========   =========================    ==============     ======================================================


----------
POST /jobs
----------

The POST action is used to insert a new job into the pipeline.
You need to send JSON data with specific information about the job::


    {
        "payload": {
            "model": "model data",            // this is of course flawed for larger modles
            "metadata": "metadata",           // and only for compatiblity
            "zip": "binary zip contents"  // as long as we don't have users and persistence
            "url": "http://someurl.to/model.zip",  // alternative to the above
        },

        // the bundle name to be used for this job
        // in the future its also possible to override templte specific settings and options
        "bundle": {
            "name": "modelconvert.bundles.pop",   // this can also contain a bundle spec and related data
            "settings": {
                "aopt.pop": true,
                "aopt.command": "{command} {input} {output} -what -ever={0} -is -required",
                "meshlab.enabled": false,
            }
        }
    }


-------------------
GET /jobs/<task-id>
-------------------







