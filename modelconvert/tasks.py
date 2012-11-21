import os
import shutil
from contextlib import closing
from zipfile import ZipFile, ZIP_DEFLATED
from subprocess import call

# template system
from jinja2 import Environment, FileSystemLoader, PackageLoader

# async tools
from celery import Celery
from celery import current_task
from celery.utils.log import get_task_logger

# app config
import settings

logger = get_task_logger(__name__)

AOPT_BINARY = getattr(settings, 'AOPT_BINARY', 'aopt')
DOWNLOAD_PATH = getattr(settings, 'DOWNLOAD_PATH', '/tmp/downloads')
DEBUG = getattr(settings, 'DEBUG', False)
TEMPLATE_PATH = getattr(settings, 'TEMPLATE_PATH')

celery = Celery("tasks", 
    broker=getattr(settings, 'CELERY_BROKER_URL', 'redis://localhost:6379/0'), 
    backend=getattr(settings, 'CELERY_RESULT_BACKEND','redis'))
jinja = Environment(loader=PackageLoader('modelconvert', 'templates'))



class ConversionError(Exception):
    pass


@celery.task
def convert_model(input_file, options=None):
    """
    Task to run the model convestion. This task is written in a manner
    that is can run independently from the web application. You can call
    this task from the command line or other rich gui. The only requirement
    is a settings module in the current package as well as the requierd 
    dependencies (celery, jinja, aopt, meshlab, etc.).
    
    TODO:
      - make directories hash.tmp and rename after successfull transcoding
        this is to distinguish between orphaned files and completed ones
    """
    # The current tasks id
    task_id = current_task.request.id
    
    # options:
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
    
    # alternative template
    template = options.get('template', None)
    
    # aopt options
    aopt = options.get('aopt', None)

    # return OK or FAILED as well as hash for info where to 
    # find generated files
    logger.info("Starting to process uploaded file: {0}".format(input_file))

    output_directory = os.path.join(DOWNLOAD_PATH, hash)
    os.mkdir(output_directory)
    
    if template and template == 'fullsize' or template == 'metadataBrowser':
        output_extension = '.x3d'
        aopt_switch = '-x'

        # render the template with inline
        output_template_filename = os.path.join(DOWNLOAD_PATH, 
                                                hash, hash + '.html')

        logger.info("HELLO" +os.path.join(TEMPLATE_PATH, template +'/' + template + '_template.html'))
        user_tpl = jinja.get_template(template +'/' + template + '_template.html')
        
        with open(output_template_filename, 'w+') as f:
            f.write(user_tpl.render(X3D_INLINE_URL='%s.x3d' % hash))

        output_directory_static = os.path.join(output_directory, 'static')
        input_directory_static = os.path.join(TEMPLATE_PATH, template, 'static')

        shutil.copytree(input_directory_static, output_directory_static)
        
        # copy metadata to output dir if present
        meta_filename = options.get('meta_filename', None)
        if meta_filename:
            shutil.copy(meta_filename, output_directory)

    else:
        output_extension = '.html'
        aopt_switch = '-N'

    output_filename = hash + output_extension
    working_directory = os.getcwd()
    os.chdir(output_directory)
    
    logger.info("Output filename:   {0}".format(output_filename) )
    logger.info("Output directory: {0}".format(output_directory) )
    logger.info("Working directory: {0}".format(working_directory) )

    if aopt == 'restuctedBinGeo':
        output_directory_binGeo = os.path.join(output_directory, "binGeo")
        os.mkdir(output_directory_binGeo)
        
        status = call([
          AOPT_BINARY, 
          "-i", 
          input_file, 
          "-u", 
          "-b", 
          hash + '.x3db'
        ])

        if status < 0:
            
            # FIXME error handling and cleanup (breaking early is good but
            # cleanup calls for try/catch/finally)
            os.chdir(working_directory)
            logger.error("Error converting file!!!!!!!!!!")
            raise ConversionError('AOPT RETURNS: {0}'.format(status))

        else:
            status = call([
              AOPT_BINARY, 
              "-i", 
              hash + '.x3db', 
              "-F", 
              "Scene",
              "-b", 
              hash + '.x3db'
            ])

        if status < 0:
            # FIXME error handling and cleanup (breaking early is good but
            # cleanup calls for try/catch/finally)
            os.chdir(working_directory)
            logger.error("Error converting file!!!!!!!!!!")
            raise ConversionError('AOPT RETURNS: {0}'.format(status))
        else:
            status = call([
              AOPT_BINARY, 
              "-i", 
              hash + '.x3db', 
              "-G", 
              'binGeo/:saI',              
              aopt_switch, 
              output_filename
            ])
        
    elif aopt == 'binGeo':
        output_directory_binGeo = os.path.join(output_directory, "binGeo")
        os.mkdir(output_directory_binGeo)
        status = call([
          AOPT_BINARY, 
          "-i", 
          input_file, 
          "-G", 
          'binGeo/:saI', 
          aopt_switch, 
          output_filename
        ])


    else:  
        status = call([
          AOPT_BINARY, 
          "-i", 
          input_file, 
          aopt_switch, 
          output_filename
        ])


    
    if status < 0:
        # FIXME error handling and cleanup (breaking early is good but
        # cleanup calls for try/catch/finally)
        os.chdir(working_directory)
        logger.error("Error converting file!!!!!!!!!!")
        raise ConversionError('AOPT RETURNS: {0}'.format(status))
    else:
        zip_path = os.path.join(DOWNLOAD_PATH, hash)
        _zipdir(zip_path, '%s.zip' % hash)
        os.chdir(working_directory)
    
    if not DEBUG:
        # delete the uploaded file
        os.remove(input_file)
    
    import time
    time.sleep(10)
    result_set = dict(
        hash = hash,
        input_file = input_file,
    )
    return result_set
#    return "My task ID is {0}, hash: {1}, sourcef: {2}".format(task_id, hash, input_file)



def _zipdir(basedir, archivename):
    assert os.path.isdir(basedir)
    with closing(ZipFile(archivename, "w", ZIP_DEFLATED)) as z:
        for root, dirs, files in os.walk(basedir):
            # ignore empty directories
            for fn in files:
                # skip self and other zip files
                if os.path.basename(fn) == os.path.basename(archivename):
                    continue
                absfn = os.path.join(root, fn)
                zfn = absfn[len(basedir)+len(os.sep):] #XXX: relative path
                z.write(absfn, zfn)



if __name__ == "__main__":
#    celery.start()
    testfile = 'tests/data/flipper.x3d'
    result = convert_model.apply_async((testfile,))