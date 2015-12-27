# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import os
from glumpy.log import log

def find(name):
    """ Locate a filename into the shader library """

    if os.path.exists(name):
        return name

    path = os.path.dirname(__file__) or '.'
    filename = os.path.abspath(os.path.join(path,name))
    if os.path.exists(filename):
        return filename

    for d in os.listdir(path):
        fullpath = os.path.abspath(os.path.join(path,d))
        if os.path.isdir(fullpath):
            filename = os.path.abspath(os.path.join(fullpath,name))
            if os.path.exists(filename):
                return filename
    return None


def get(name):
    """ Retrieve code from the given filename """

    filename = find(name)
    if filename == None:
        return name
    return open(filename).read()
