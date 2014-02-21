.. _api:


===
API
===
The pipeline can be driven through the HTTP protocol using a restful approach.
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
Pipeline REST requests are HTTP requests as defined per `RFC 2616 <http://www.ietf.org/rfc/rfc2616.txt>`_.
A typical REST action consists of sending an HTTP request to the Pipeline and 
waiting for the response. Like any HTTP request, a REST request to the Pipeline
system contains a request method, a URI, request headers, and maybe a 
query string or request body. The response contains an HTTP status code, 
response headers, and maybe a response body.

To acceess the Pipeline through the API you need to send a properly encoded 
HTTP request to the service endpoint. The encoding of the request neesd to be 
UTF-8 and the mimetype needs to be set to ``application/json`` or sometimes
``application/octet-stream``. You can use  the cURL tool to test your 
requests, e.g::

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

~~~~~~~~~~~~~~~~~~~~
Payloads and Buckets
~~~~~~~~~~~~~~~~~~~~

In order to process some uploaded files by the pipeline the files need
to be stored somewhere in the first place. We achieve this by providing upload 
buckets. Think of a bucket as of a remote upload floder you can drop files to.
Much similar to a S3 bucket, but much more temporary and entirely managed by 
the pipeline service.

A payload forms the input set of files to be fed to the pipeline. Currently 
the API recognizes two different payloads types: buckets and http URLs. 
In order to distinguish the input payload type, we use the URI scheme. 
For example to feed the pipeline with the contents of a payload bucket, the 
corrcet way to tell this the API is::

    bucket://<bucket_id>

For exmaple::

    bucket://afc34398da0f890dsa890fd8s9afc

In order to use a URI as input source, just specify the http protocol, domain
and other parts e.g.::

    http://domain.tld/some/archive.zip
    http://domain.tld/some/model.ply


The storage backend can be completely transparent. In the future it is 
planned to add more storage backends to the system like Amazon S3, Glacier,
SVN, WebDAV, Hadoop, etc. For the time being only HTTP and pipeline managed
buckets are working.


~~~~
Jobs
~~~~
Jobs kick off the pipleline processing and bundle all relevant information
as well as provide a interface for interacting with a current processing job.
For exmaple get status information, pause, delete or restart a job. Jobs 
are excuted asynchronously and distributed by the Celery queue system.



---------------
Basic Workflow
---------------

The basic workflow to use the pipeline is as follows:

Post a file to the server using a bucket::

    POST /api/v1/buckets HTTP/1.1
    Accept: application/json
    Accept-Encoding: gzip, deflate, compress
    Content-Length: 12888639
    Content-Type: application/octet-stream
    Host: pipelineserver.tld
    X-Filename: test.ply

    <binary data not shown>

You get back a JSON response containing a cleartext message, a bucket ID and
the filename of your uploaded date within the bucket. Save the ID and the 
filename in your application, you will need it later. You can upload a zip file 
as well.

.. Upload more files using the bucket ID you got back from the first call::
..     POST <base_uri>/buckets/<bucket_id>
..     X-Filename: anotherfile.ply
..     Content-Type: application/octet-stream

.. note:: For the moment, use a zip file to upload multiple models and/or assets
    to the server. The POST more files to a existing bucket is not implemented yet.

Get a list of templates to select from::

    GET /api/v1/bundles
    Accept: application/json
    Accept-Encoding: gzip, deflate, compress
    Host: pipelineserver.tld

You can alos perform this step before uploading. For exmaple you could
call the URL one time your application starts and cache the results. 
You will want to use the "name" field of the template you want to use
for processing when starting a job.

Add a job to the processing queue and start it::

    POST /api/v1/jobs
    Accept: application/json
    Accept-Encoding: gzip, deflate, compress
    Host: pipelineserver.tld

    {
        "payload": "bucket://<bucket_id>",
        "payload_filename": "herkules.ply",
        "template": "basic"
    }

You will get back more information about this job::

    {
        "task_id": "123",
        "job_url":   "full.host/v1/jobs/123",       
        "progress_url": "full.host/v1/stream/123"
    }

The most imporant information is the ``job_url`` which is used to freuqently 
query the backend about the status of a job::

    GET /api/v1/jobs/123
    Accept: application/json
    Accept-Encoding: gzip, deflate, compress
    Host: pipelineserver.tld

Do not query the pipeline to often this way (about every 5-10 seconds is 
proabably enough). To save transport overhead, you can resport to making a 
HEAD request only in order to check status. If status is 200 then you
can issue an addtional request to get the rest of the information.

Additionally you can make use of the ``progress_url`` to get realtime-push 
messages about the status. This URL implements the EventSource push protocol.

.. warning:: Do not use the push messages to determine if the conversion is complete 
    as they are not relieable enougth to do so.

In case the job is still running a simple HTTP code of 102 is returend.
If the job completed you will get a 200 return code as well as the following
information::

    {   
        "download_url":"http:/domain.tld/somplace/download.zip",
        "preview_url": "htt://domain.tld/someplace/index.html"
    }

With the download and preview URLs you then can get the completed job
output and download it or redirect a browser to the preview HTML page.

All URLs returned by the API are absolute, you do not need to keep track
of base URLs, just use the returend values.

For a detailed and up-to date description of JSON fields and responses, 
see below.


--------
Overview
--------

===========   =========================    =================     ==========================================================
 HTTP verb     URI                          Return codes          Description
===========   =========================    =================     ==========================================================
GET            /                            200                   API version, help URL and other relevant information
GET            /bundles                     200                   Returns a JSON formatted list of application bundles
GET            /buckets                     200,404               NOOP: A list of payload buckets so far
POST           /buckets                     201,500,420,415       Upload a file to the server which creates a bucket
GET            /buckets/<bucket-id>         200,404               NOOP: A list of files in the bucket with the resp. ID
POST           /buckets/<bucket-id>         ^ + 201, 404          NOOP: Upload another file to a specific resource bucket
                                                                  (noop as of yet)
GET            /jobs                        200,404               Returns a list of jobs, 404 if no jobs are found
POST           /jobs                        201,400,416,403       Add a new job to the queuing system. By default
                                                                  processing starts immediately.
GET            /jobs/<task-id>              200, 102              Returns status of a job with given GUID. Will return 
                                                                  HTTP status code 102 if the job can't be found or is 
                                                                  still processing.
                                                                  Returns a 200 if job did complete.
                                                                  You can make a HEAD request without sending
                                                                  data to make the lookup quicker.
                                                                  If the job did complete, JSON response includes
                                                                  details.
                                                                  It is probably best to not query the backend
                                                                  too often (maybe every 5 seconds).
GET            /stream/<task-id>/                                 Live updates of processing events. This endpoint
                                                                  provides a push service with EventSource type 
                                                                  messages. It can be used to display realtime status
                                                                  messages.
===========   =========================    =================     ==========================================================



-------------
POST /buckets
-------------
.. autofunction:: modelconvert.api.views.add_bucket()


-------------------------
POST /buckets/<bucket_id>
-------------------------
.. autofunction:: modelconvert.api.views.add_to_bucket()


----------
POST /jobs
----------

.. autofunction:: modelconvert.api.views.add_job()

-------------------
GET /jobs/<task-id>
-------------------

.. autofunction:: modelconvert.api.views.job_status()

----------------------
GET /stream/<task-id>/
----------------------

.. autofunction:: modelconvert.api.views.stream()