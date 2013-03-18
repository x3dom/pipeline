# -*- coding: utf-8 -*-
"""
This file contains celery tasks that are used to async the process of 
converting models. It is required that celery runs within a falsk
app context in order to execute the tasks.

You can achieve this by createing a instance of the app and then use a
context manager to run celery. For example:

    from modelconvert import create_app
    from modelconvert.extensions import celery

    app = create_app()

    with app.app_context():
        celery.worker_main(['worker', '-E', '-l', 'INFO'])

"""
import os
import shutil
import subprocess
import zipfile
import datetime

from flask import current_app
from celery import current_task

from jinja2 import Environment, FileSystemLoader

from modelconvert.extensions import celery, red
from modelconvert.utils import compression


class ConversionError(Exception):
    pass


def update_progress(msg):
    """
    Updates custom PROGRESS state of task. Also sends a message to the subpub
    channel for status updates. We EventSource push notification so reduce
    server load. The custom PROGRESS state is used for XHR poll fallback.
    """
    current_app.logger.debug(msg)
    current_task.update_state(state='PROGRESS', meta={'message': msg})

    #now = datetime.datetime.now().replace(microsecond=0).time()
    current_app.logger.info("Sening to redis: {0}".format(current_task.request.id))
    red.publish(current_task.request.id, '{0}'.format(msg))



@celery.task
def ping():
    """ Just for testing """
    log = current_app.logger
    log.info("+++++++++ PING +++++++++")

def cleanup():
    """Stub for celerybeat task to clean out previews"""
    pass

@celery.task
def assemble_deliverable(path_to_converted_files, tempalate_bundle, options=None):
    """Stub"""
    pass


@celery.task
def convert_model(input_file, options=None):
    """
    Task to run the model convestion. This task is written in a manner
    that is can run independently from the web application. You can call
    this task from the command line or other rich gui. The only requirement
    is a settings module in the current package as well as the requierd 
    dependencies (celery, jinja, aopt, meshlab, etc.).
    
    This tasks is currently very monolithic and does too much.
    To make this more flexible, this task should really only convert
    and optimize one file. If multiple files are uploaded, tasks
    can be chained. Also assembly of templates should not go here.


    TODO:
      - make directories hash.tmp and rename after successfull transcoding
        this is to distinguish between orphaned files and completed ones
    """

    update_progress("Warming up...")

    # need this so pubsub will work, it's probably due to too fast processing
    # and the reconn timout of evensource
    # FIXME find out why we need to wait a bit and fix it
    import time
    time.sleep(4)

    log = current_app.logger

    # The current tasks id
    task_id = current_task.request.id
    
    # options:
    #   meshlab
    #   template
    #   hash
    #   meta
    
    # keep the generated hash for filenames
    # use the taskid for status only
    # delted uploaded file on successfull conversion, otherwise
    # log filename in error trace
    
    # the hash should always be provided, however if not
    # i.e. running outside a web application, we use the taskid
    hash = options.get('hash', task_id)

    # meshlab options
    meshlab = options.get('meshlab', None)
    
    # alternative template
    template = options.get('template', None)
    
    # aopt options
    aopt = options.get('aopt', None)

    update_progress("Starting to process uploaded file")
    log.info("Uploaded file: {0}".format(input_file))

    # {{{ start code which will be refactored to frontend 
    # If the uploaded file is a archive, uncompress it.
    # Note that this step should be moved to the controller once we support
    # a wizard style: upload file, select template, analyze contents and present
    # options for each model. but for now, we are using the naive approach.
    if compression.is_archive(input_file):
        update_progress("Input file is a (compressed) archive. Trying to deflate...")


    # }}}


    download_path = current_app.config['DOWNLOAD_PATH']
    template_path = current_app.config['TEMPLATE_PATH']
    upload_path = current_app.config['UPLOAD_PATH']
    
    # specifically not using the current_app.jinja_env in order to seperate
    # user templates entirely from the application. The user should not have
    # access to the request, global object and app configuration.
    jinja = Environment(loader=FileSystemLoader(template_path))

    output_directory = os.path.join(download_path, hash)
    os.mkdir(output_directory)
    
    if template and template == 'fullsize' or template == 'metadataBrowser':
        output_extension = '.x3d'
        aopt_output_switch = '-x'

        # render the template with inline
        output_template_filename = os.path.join(download_path, 
                                                hash, hash + '.html')
        user_tpl = jinja.get_template(template +'/' + template + '_template.html')
        
        with open(output_template_filename, 'w+') as f:
            f.write(user_tpl.render(X3D_INLINE_URL='%s.x3d' % hash))

        output_directory_static = os.path.join(output_directory, 'static')
        input_directory_static = os.path.join(template_path, template, 'static')

        shutil.copytree(input_directory_static, output_directory_static)
        
        # copy metadata to output dir if present
        meta_filename = options.get('meta_filename', None)
        if meta_filename:
            shutil.copy(meta_filename, output_directory)

    else:
        output_extension = '.html'
        aopt_output_switch = '-N'

    output_filename = hash + output_extension
    working_directory = os.getcwd()
    os.chdir(output_directory)
    
    log.info("Output filename:   {0}".format(output_filename) )
    log.info("Output directory: {0}".format(output_directory) )
    log.info("Working directory: {0}".format(working_directory) )
    log.info("Aopt binary: {0}".format(current_app.config['AOPT_BINARY']))
    log.info("Meshlab binary: {0}".format(current_app.config['MESHLAB_BINARY']))

    #inputfile = outputfile warning
    
    
    if meshlab:
        
        update_progress("Meshlab optimization...")
        
        env = os.environ.copy()
        env['DISPLAY'] = current_app.config['MESHLAB_DISPLAY']
        
        mehlab_filter = ""
        mehlab_filter += "<!DOCTYPE FilterScript><FilterScript>"

        for item in meshlab:
            mehlab_filter += '<filter name="' + item + '"/>' 

        mehlab_filter += "</FilterScript>"

        mehlab_filter_filename = os.path.join(current_app.config['UPLOAD_PATH'], hash + '.mlx')
        filter_file = open(mehlab_filter_filename, "w") 
        filter_file.write(mehlab_filter) 
        filter_file.close()
        
        # Subprocess in combination with PIPE/STDOUT could deadlock
        # be careful with this. Prefer the Python 2.7 version below or
        # maybe switch to using envoy or similar.
        proc = subprocess.Popen([
            current_app.config['MESHLAB_BINARY'], 
            "-i", 
            input_file, 
            "-o",
            input_file, 
            "-s",
            mehlab_filter_filename,
            "-om",
            "ff"
            ],
            env=env, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT)
        
        out = proc.communicate()[0]
        returncode = proc.wait()

        log.info("Meshlab optimization {0}".format(returncode))
        log.info(out)

        if returncode == 0:
            update_progress("Meshlab successfull")
        else:
            update_progress("Meshlab failed!")
            log.error("Meshlab problem exit code {0}".format(returncode))

        # Python 2.7
        # try:
        #     check_output([
        #         current_app.config['MESHLAB_BINARY'], 
        #         "-i", 
        #         input_file, 
        #         "-o",
        #         input_file, 
        #         "-s",
        #         mehlab_filter_filename,
        #         "-om",
        #         "ff"
        #         ], env=env)
        #         
        # except CalledProcessError as e:
        #     log.info("Meshlab problem exit code {0}".format(e.returncode))
        #     log.error("Meshlab: " + e.output)
            

        # if status == 0:
        #     log.info("Meshlab optimization {0}".format(status))
        # else:
        #     log.info("Meshlab problem exit code {0}".format(status))

    else:
       update_progress("Skipping Meshlab optimization")


    update_progress("Starting AOPT conversion")

    if aopt == 'restuctedBinGeo':
        update_progress("AOPT restructured binary geo optimization...")


        output_directory_binGeo = os.path.join(output_directory, "binGeo")
        os.mkdir(output_directory_binGeo)

        #aopt -i input.ply -F Scene:"maxtris(23000)" -f PrimitiveSet:creaseAngle:4
        # -f PrimitiveSet:normalPerVertex:TRUE -f PrimitiveSet:optimizationMode:none
        # -V -G binGeo/:sacp -x model.x3d -N model.html
        status = subprocess.call([
            current_app.config['AOPT_BINARY'], 
            '-i', 
            input_file, 
            '-F',
            'Scene:"maxtris(23000)"', 
            '-f',
            'PrimitiveSet:creaseAngle:4',              
            '-f'
            'PrimitiveSet:normalPerVertex:TRUE',
            '-f',
            'PrimitiveSet:optimizationMode:none',
            '-V',
            '-G ',
            'binGeo/:sacp',
            aopt_output_switch, 
            output_filename
        ])
        
    elif aopt == 'binGeo':
        update_progress("AOPT binary geo optimization...")
        output_directory_binGeo = os.path.join(output_directory, "binGeo")
        os.mkdir(output_directory_binGeo)
        status = subprocess.call([
          current_app.config['AOPT_BINARY'], 
          "-i", 
          input_file, 
          "-G", 
          'binGeo/:saI', 
          aopt_output_switch, 
          output_filename
        ])

    else:  

        update_progress("AOPT standard conversion in progress...")

        status = -100
        aopt_cmd = [
            current_app.config['AOPT_BINARY'], 
            "-i", 
            input_file, 
            aopt_output_switch, 
            output_filename
        ]

        try:
            status = subprocess.call(aopt_cmd)
        except OSError:
            update_progress("Failure to execute AOPT")
            err_msg = "Error: AOPT not found or not executable {0}".format(repr(aopt_cmd))
            log.error(err_msg)
            raise ConversionError(err_msg)


    if status < 0:
        # FIXME error handling and cleanup (breaking early is good but
        # cleanup calls for try/catch/finally or contextmanager)
        os.chdir(working_directory)

        # fixme: put this in exception code
        update_progress("Error on conversion process")
        log.error("Error converting file!!!!!!!!!!")
        raise ConversionError('AOPT RETURNS: {0}'.format(status))
    else:
        update_progress("Assembling deliverable...")
        zip_path = os.path.join(download_path, hash)
        compression.zipdir(zip_path, '%s.zip' % hash)
        os.chdir(working_directory)
    
    if not current_app.config['DEBUG']:
        # delete the uploaded file
        update_progress("Cleaning up...")
        os.remove(input_file)
    
    # import time
    # time.sleep(10)
    result_set = dict(
        hash = hash,
        input_file = input_file,
    )
    return result_set
