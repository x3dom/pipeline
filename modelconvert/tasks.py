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
from celery.utils.log import get_task_logger

#logger = get_task_logger(__name__)

from jinja2 import Environment, FileSystemLoader, TemplateNotFound

from modelconvert import security
from modelconvert.extensions import celery, red
from modelconvert.utils import compression, fs

class ConversionError(Exception):
    pass


# class TaskProgress(object):

#     ERROR = -1
#     INFO = 0
#     WARNING = 1

#     def update(self, message, level=INFO):
#         pass




def update_progress(msg):
    """
    Updates custom PROGRESS state of task. Also sends a message to the subpub
    channel for status updates. We EventSource push notification so reduce
    server load. The custom PROGRESS state is used for XHR poll fallback.
    """
    current_app.logger.info("(+++) PROGRESS: {0} (TASK: {1})".format(msg, current_task.request.id))
    current_task.update_state(state='PROGRESS', meta={'message': msg})
    #now = datetime.datetime.now().replace(microsecond=0).time()
    red.publish(current_task.request.id, '{0}'.format(msg))



@celery.task
def ping():
    """ Just for testing """
    logger.info("+++++++++ PING +++++++++")


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
    can be chained.

    This task is currently a spaghetti monster mess from hell.
    """

    update_progress("Warming up...")

    # # need this so pubsub will work, it's probably due to too fast processing
    # # and the reconn timout of evensource
    # # FIXME find out why we need to wait a bit and fix it
    # import time
    # time.sleep(10)

    logger = current_app.logger

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
    # i.e. running outside a web application, we reuse the taskid
    hash = options.get('hash', task_id)

    # meshlab options
    meshlab = options.get('meshlab', None)
    
    # alternative template
    template = options.get('template', 'basic')

    # copy metadata to output dir if present
    meta_filename = options.get('meta_filename', None)


    # get the filename without extension 
    # i.e. /path/tp/foo.obj     -> foo
    #      /path/tp/foo.bar.obj -> foo.bar
    # FIXME: get rid of this, in case of zip file this is hash.zip
    # and not usable the way we use it right now
    input_filename = os.path.splitext(os.path.basename(input_file))[0]


    update_progress("Starting to process uploaded file")
    logger.info("Uploaded file: {0}".format(input_file))

    download_path = current_app.config['DOWNLOAD_PATH']
    bundles_path = current_app.config['BUNDLES_PATH']
    upload_path = current_app.config['UPLOAD_PATH']

    # this should actuayll come in as parameter, as we assume too much here
    upload_directory = os.path.join(current_app.config['UPLOAD_PATH'], hash)
    
    # first create where everything is stored
    output_directory = os.path.join(download_path, hash)
    os.mkdir(output_directory)


    # {{{ ZIPFILES
    # If the uploaded file is a archive, uncompress it.
    # Note that this step should be moved to the controller (or another task)
    # once we switch to a different workflow (upload file->select template->convert)
    # for each model. but for now, we are using the naive approach.
    # refactor this out
    

    # format ('infile.obj','outfile.x3d', ['outfile.xml'] or None)
    # it might make sense to create a class or at least a dict for this 
    # in the future,
    models_to_convert = []  

    if compression.is_archive(input_file):
        update_progress("Umcompressing archive")
        
        uncompressed_path = upload_directory + '.tmp'
        os.mkdir(uncompressed_path)

        compression.unzip(input_file, uncompressed_path)

        update_progress("Archive uncompressed")

        resources_to_copy =  []  # etnry format path/to/resource
        found_models = [] 
        found_metadata = []

        update_progress("Detecting models and resources")

        # detect and collect models, metadata, and resources
        for root, dirs, files in os.walk(uncompressed_path, topdown=False):
            for name in files:
                if security.is_model_file(name):
                    update_progress("Found model: {0}".format(name))
                    found_models.append(name)
                elif security.is_meta_file(name):
                    update_progress("Found meta data: {0}".format(name))
                    found_metadata.append(name)
                else:
                    update_progress("Found resource: {0}".format(name))
                    resources_to_copy.append(name)
                    # just copy over
                    
            for name in dirs:
                update_progress("Found directory: {0}".format(name))
                resources_to_copy.append(name)

        if not found_models:
            raise ConversionError("No models found in archive. Be sure to put all models at the root level of your archive.")

        logger.info("****** FOUND_META: {0}".format(found_metadata))

        update_progress("Associating meata data to models")

        # FIXME: this could be improved
        for model in found_models:
            m_root = os.path.splitext(os.path.basename(model))[0]

            m_output_inline = m_root + '.x3d'
            m_output_html = m_root + '.html'

            # now we have a list of metas belonging to the current model
            # store that in the master list
            model_base_split = os.path.splitext(os.path.basename(model))
            model_info_dict = {
                'name':   model_base_split[0],

                'input':  model,
                'input_format': model_base_split[1][1:], # fixme, use magic|mime instead of extension
                'input_path': os.path.abspath(uncompressed_path),

                'output': model_base_split[0] + '.x3d',
                'output_format': 'x3d',
                
                'inline': model_base_split[0] + '.x3d',
                'preview': model_base_split[0] + '.html',
                
                'resources': resources_to_copy,
            }

            # then walk each metadata to find match for model
            m_metas = []
            for r in found_metadata:
                # found matching metadata file, mark it
                r_root = os.path.splitext(os.path.basename(r))[0]
                r_ext = os.path.splitext(os.path.basename(r))[1][1:]
                if r_root == m_root:
                    m_metas.append({
                        'file': r,
                        'type': r_ext,
                    })

            if m_metas:
                model_info_dict.update(metadata=m_metas)

            models_to_convert.append(model_info_dict)
#            models_to_convert.append( (model, m_output_inline, m_output_html, m_metas,) )

        # we now have list of models with associated metadata
        # and a list of plain resources that simply need to be copied
        #   models_to_convert
        #   resources_to_copy
        logger.info("****** MODELS: {0}".format(models_to_convert))
        logger.info("****** RESOURCES: {0}".format(resources_to_copy))
        

        ####### First copy the resources

        # simplified: we just copy everything that is dir blindly as well
        # as all files in the root level which are not models.
        for resource in resources_to_copy:
            src = os.path.join(uncompressed_path, resource)
            dest = os.path.join(output_directory, resource)

            if os.path.isdir(src):
                fs.copytree(src, dest)
            else:
                shutil.copy(src, dest)
    # }}}
    else:
        # no compression, no multimodel, no, textures..
        current_input_filename = os.path.splitext(os.path.basename(input_file))[0]

        model_base_split = os.path.splitext(os.path.basename(input_file))
        model_info_dict = {
            'name':   model_base_split[0],

            'input':  os.path.basename(input_file),
            'input_format': model_base_split[1][1:], # fixme, use magic|mime instead of extension
            'input_path': os.path.abspath(os.path.dirname(input_file)),

            'output': model_base_split[0] + '.x3d',
            'output_format': 'x3d',
            
            'inline': model_base_split[0] + '.x3d',
            'preview': model_base_split[0] + '.html',
            
            'resources': None,
        }

        # we have a meta file which could be named whatever, normalize
        # this is a mess - but for the review...
        if meta_filename:
            
            meta_dest_filename = input_filename + os.path.splitext(meta_filename)[1]
            shutil.copy(meta_filename, os.path.join(output_directory, meta_dest_filename))

            meta_data_list = [{
                'file': meta_dest_filename,
                'type': os.path.splitext(meta_filename)[1],
            }],

            model_info_dict.update(metadata=meta_data_list)

        models_to_convert.append(model_info_dict);
        logger.info("***** MODELS TO CONVERT: {0} ".format(models_to_convert))

#        models_to_convert = [ (input_file, current_input_filename+'.x3d', current_input_filename+'.html', meta_dest_filename) ]



    logger.info("***** MODELS TO CONVERT: {0} ".format(models_to_convert))

    # ------------------------------------------------------------------
    # The following steop only generates templates, for the uploaded
    # data. This can be refactored out. The reason this runs before aopt
    # is in order to allow live preview of partially optimized models later
    # on. 

    # first copy static assets
    output_directory_static = os.path.join(output_directory, 'static')
    input_directory_static = os.path.join(bundles_path, template, 'static')
    input_directory_shared = os.path.join(bundles_path, '_shared')
        
    # copy shared resources
    fs.copytree(input_directory_shared, output_directory)

    # copy template resources
    fs.copytree(input_directory_static, output_directory_static)


    # init template engine
    jinja = Environment(loader=FileSystemLoader(os.path.join(bundles_path, template)))

    tpl_job_context = {
        # fixme assuming too much here
        'archive_uri': hash + '.zip'
    }

    list_template = 'list.html'
    model_template = 'view.html'

    # first render index template if it's present in the template bundle.
    # we always do this, even if there's only one model to convert
    try:
        update_progress("Starting to render list template")

        tpl = jinja.get_template(list_template)
        context = { }
        context.update(models=models_to_convert, job=tpl_job_context)
        # we need info on the models, probably a object would be nice

        tpl_output = os.path.join(output_directory, 'list.html')
        # finally render template bundle
        with open(tpl_output, 'w+') as f:
            f.write(tpl.render(context))

    except TemplateNotFound as tplnf:
        # not sure if we should stop here, for the moment we proceed
        # since the list.html list view is technically not necessary
        # to complete rendering
        update_progress("List template not found, proceeding without")
        logger.error("Template '{0}' not found - ignoring list view".format(list_template))
    finally:
        update_progress("Done processing list template")

    
    model_template_context = dict()
    try:
        model_template_renderer = jinja.get_template(model_template)

        for model in models_to_convert:
            # now render templates for individual models
            update_progress("Rendering template for model: {0}".format(model['name']))

            # write out template
            model_template_context.update(
                model=model,
                # the job this model belongs to (used for getting archive name)
                job=tpl_job_context  
            )

            tpl_output = os.path.join(output_directory, model['preview'])
            with open(tpl_output, 'w+') as f:
                f.write(model_template_renderer.render(model_template_context))

    except TemplateNotFound:
        logger.error("Template '{0}'' not found - ignoring list view".format(view_template))
    


    ### temp
    output_filename = models_to_convert[0]['output']
    output_template_filename = models_to_convert[0]['preview']


    # end template generation
    # ------------------------------------------------------------------


    # ------------------------------------------------------------------
    # Meshlab doing it's thing, generating temproary outputs
    # this should live in its own task
    # ------------------------------------------------------------------
    working_directory = os.getcwd()
    os.chdir(output_directory)
    
    logger.info("Output filename:   {0}".format(output_filename) )
    logger.info("Output directory: {0}".format(output_directory) )
    logger.info("Working directory: {0}".format(working_directory) )
    logger.info("Aopt binary: {0}".format(current_app.config['AOPT_BINARY']))
    logger.info("Meshlab binary: {0}".format(current_app.config['MESHLAB_BINARY']))

    
    if meshlab:
        #inputfile = outputfile could lead to problems later on
        
        update_progress("Meshlab optimization...")
        
        env = os.environ.copy()
        env['DISPLAY'] = current_app.config['MESHLAB_DISPLAY']

                
        mehlab_filter = ""
        mehlab_filter += "<!DOCTYPE FilterScript><FilterScript>"

        for item in meshlab:
            # fixme, parameterization could be dynamic, not hardcoded
            if item == "Remove Isolated pieces (wrt Face Num.)":
                mehlab_filter += '<filter name="' + item + '">'
                mehlab_filter += '<Param type="RichInt" value="50" name="MinComponentSize"/>'
                mehlab_filter += '</filter>'
            else:
                mehlab_filter += '<filter name="' + item + '"/>' 

        mehlab_filter += "</FilterScript>"



        # todo-> name this after model
        mehlab_filter_filename = os.path.join(output_directory, hash + '.mlx')
        with open(mehlab_filter_filename, 'w+') as f:
            f.write(mehlab_filter)
        
        # Subprocess in combination with PIPE/STDOUT could deadlock
        # be careful with this. Prefer the Python 2.7 version below or
        
        for model in models_to_convert:
            update_progress("Meshlab optimization: {0}".format(model['input']))
            
            meshalb_input_file = os.path.join(model['input_path'], model['input'])

            proc = subprocess.Popen([
                current_app.config['MESHLAB_BINARY'], 
                "-i", 
                meshalb_input_file, 
                "-o",
                meshalb_input_file, 
                "-s",
                mehlab_filter_filename,
                "-om",
                "ff"
                ],
                env=env, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT)
            
            output = proc.communicate()[0]
            returncode = proc.wait()

            # create a aopt log in debug mode
            if current_app.config['DEBUG']:
                with open(os.path.join(output_directory, 'meshlab.log'), 'a+') as f:
                    f.write(output)


            logger.info("Meshlab optimization model: {0} return: {1}".format(meshalb_input_file, returncode))
            logger.info(output)

            if returncode == 0:
                update_progress("Meshlab successfull")
            else:
                update_progress("Meshlab failed!")
                logger.error("Meshlab problem: {0} return: {1}".format(meshalb_input_file, returncode))

        

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
        #     logger.info("Meshlab problem exit code {0}".format(e.returncode))
        #     logger.error("Meshlab: " + e.output)
            

        # if status == 0:
        #     logger.info("Meshlab optimization {0}".format(status))
        # else:
        #     logger.info("Meshlab problem exit code {0}".format(status))

    else:
       update_progress("Skipping Meshlab optimization")


    # end Meshlab
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # Aopt call
    # this should live in its own task (or maybe transcoder in the future)
    # ------------------------------------------------------------------
    update_progress("Starting AOPT conversion")

    status = -100

    for model in models_to_convert:

        update_progress("Converting: {0}".format(model['input']))

        aopt_bingeo = "{0}_bin".format(model['name'])
        os.mkdir(os.path.join(output_directory, aopt_bingeo))

        infile  = os.path.join(model['input_path'], model['input'])
        outfile = os.path.join(output_directory, model['output'])

        aopt_cmd = [
            current_app.config['AOPT_BINARY'], 
            '-i', 
            infile, 
            '-F',
            'Scene:"cacheopt(true)"',
            '-f',
            'PrimitiveSet:creaseAngle:4',              
            '-f'
            'PrimitiveSet:normalPerVertex:TRUE',
            '-V',
            '-G',
            aopt_bingeo + '/:sacp',
            '-x', 
            outfile
        ]

        try:
        
            update_progress("Running AOPT")
            #status = subprocess.call(aopt_cmd)


            process = subprocess.Popen(aopt_cmd, 
               stdout=subprocess.PIPE, 
               stderr=subprocess.STDOUT) 
            output = process.communicate()[0] 

            status = process.wait()

            # create a aopt log in debug mode
            if current_app.config['DEBUG']:
                with open(os.path.join(output_directory, 'aopt.log'), 'a+') as f:
                    f.write(output)


            logger.info("Aopt return: {0}".format(status))
            logger.info(output)

        except OSError:
            update_progress("Failure to execute AOPT")
            err_msg = "Error: AOPT not found or not executable {0}".format(repr(aopt_cmd))
            logger.error(err_msg)
            raise ConversionError(err_msg)


    if status < 0:
        # FIXME error handling and cleanup (breaking early is good but
        # cleanup calls for try/catch/finally or contextmanager)
        os.chdir(working_directory)

        # fixme: put this in exception code
        update_progress("Error on conversion process")
        logger.error("Error converting file!!!!!!!!!!")
        raise ConversionError('AOPT RETURNS: {0}'.format(status))
    
    else:
        # ------------------------------------------------------------------
        # Final creation of deliverable, could live in it's own task
        # ------------------------------------------------------------------
        update_progress("Assembling deliverable...")
        zip_path = os.path.join(download_path, hash)
        compression.zipdir(zip_path, '%s.zip' % hash)

        os.chdir(working_directory)
    


    # ------------------------------------------------------------------
    # cleaning up
    # ------------------------------------------------------------------

    if not current_app.config['DEBUG']:
        # delete the uploaded file
        update_progress("Cleaning up...")

        # todo remove upload directory
        if os.path.exists(uncompressed_path):
            shutil.rmtree(uncompressed_path)
        if os.path.exists(upload_directory):
            shutil.rmtree(upload_directory)

    update_progress("Done")
    
    # import time
    # time.sleep(10)

    if len(models_to_convert) > 1:
        preview = 'list.html'
    else:
        preview = models_to_convert[0]['preview']

    result_set = dict(
        hash = hash,
        filenames = [preview, '%s.zip' % hash],
        input_file = input_file,
    )
    return result_set
