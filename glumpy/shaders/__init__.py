# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import os
from glumpy.log import log

def get_file(name):
    """ Retrieve a shader full path from sub-directories """

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

    log.warning("Shader '%s' not found" % name)
    return None


def get_code(name):
    """ Retrieve a shader code from sub-directories """

    filename = get_file(name)
    if filename:
        return open(filename).read()
    return ""
