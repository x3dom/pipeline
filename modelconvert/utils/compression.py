# -*- coding: utf-8 -*-
import os

from contextlib import closing
from zipfile import ZipFile, ZIP_DEFLATED

from . import fs

# check for securuit i.g. ../../../../etc/passwd
def unzip(file, destdir=None):
    """
    Unzips a file to a given directory
    """
    with closing(ZipFile(file)) as z:
        for name in z.namelist():
            (dirname, filename) = os.path.split(name)
            if filename == '':
                if '..' in dirname:
                    dirname = dirname.replace('..', '')

                if dirname.startswith('/'):
                    dirname = '_unkown_directory_'

                # directory
                if destdir:
                    dirname = os.path.join(destdir, dirname)
                if not os.path.exists(dirname):
                    fs.mkdir_p(dirname)
            else:
                # file
                if destdir:
                    destname = os.path.join(destdir, name)
                with open(destname, 'wb') as fd:
                    fd.write(z.read(name))


def zipdir(basedir, archivename):
    """
    Zips a directory recursively.
    """
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
