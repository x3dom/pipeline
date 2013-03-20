# -*- coding: utf-8 -*-

import urlparse

from flask import current_app


def is_allowed_archive(filename):
    """ Check if a filename is a allowed archive """
    return '.' in filename and filename.rsplit('.', 1)[1] in \
        current_app.config['SUPPORTED_ARCHIVE_EXTENSIONS']


def is_meta_file(filename):
    """ Check if a filename is a supported meta file """
    return '.' in filename and filename.rsplit('.', 1)[1] in \
        current_app.config['SUPPORTED_META_EXTENSIONS']

def is_model_file(filename):
    """ 
    Check if a filename has an supported models extension 
    This is not a surefire way to detect if the file is a model, but
    acts as basic guard and guideline.
    """
    return '.' in filename and filename.rsplit('.', 1)[1] in \
        current_app.config['SUPPORTED_MODEL_EXTENSIONS']


def is_allowed_file(filename):
    """ Check if a filename has an allowed extension """
    return '.' in filename and filename.rsplit('.', 1)[1] in \
        current_app.config['ALLOWED_EXTENSIONS']

def is_allowed_host(url):
    """ Check if a URL download is allowed """
    if "*" in current_app.config['ALLOWED_DOWNLOAD_HOSTS']:
        return True
    
    host = urlparse.urlparse(url).netloc
    return host in current_app.config['ALLOWED_DOWNLOAD_HOSTS']