# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import os
import numpy as np
from glumpy.log import log


def _get_file(name):
    """ Retrieve a data full path from sub-directories """

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
    """ Retrieve data content from a name """

    filename = _get_file(name)
    extension = os.path.basename(name).split('.')[-1]

    if extension == 'npy':
        return np.load(filename)

    log.warning("Data not found(%s)" % name)
    return None
