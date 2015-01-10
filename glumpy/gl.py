# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import ctypes
from glumpy.log import log
from OpenGL.arrays import numpymodule

try:
    numpymodule.NumpyHandler.ERROR_ON_COPY = True
except TypeError:
    log.warn("Cannot set error on copy on GPU copy")


from OpenGL import contextdata
def cleanupCallback( context=None ):
    """Create a cleanup callback to clear context-specific storage for the current context"""
    def callback( context = contextdata.getContext( context ) ):
        """Clean up the context, assumes that the context will *not* render again!"""
        contextdata.cleanupContext( context )
    return callback

from OpenGL.GL import *
from OpenGL.GL.EXT.geometry_shader4 import *
from OpenGL.GL.NV.geometry_program4 import *
from OpenGL.GL.ARB.texture_rg import *


# Patch: pythonize the glGetActiveAttrib
_glGetActiveAttrib = glGetActiveAttrib
def glGetActiveAttrib(program, index):
    # Prepare
    bufsize = 32
    length = ctypes.c_int()
    size = ctypes.c_int()
    type = ctypes.c_int()
    name = ctypes.create_string_buffer(bufsize)
    # Call
    _glGetActiveAttrib(program, index,
                       bufsize, ctypes.byref(length), ctypes.byref(size),
                       ctypes.byref(type), name)
    # Return Python objects
    return name.value, size.value, type.value


# # --- Wrapper ---
# import sys
# def wrap(name):
#     if callable(globals()[name]):
#         def wrapper(*args, **kwargs):
#             # print "Calling %s%s" % (name, args)
#             return globals()[name](*args, **kwargs)
#         return wrapper
#     else:
#         return globals()[name]
#
# class Wrapper(object):
#     def __init__(self, wrapped):
#         self.wrapped = wrapped
#     def __getattr__(self, name):
#         return wrap(name)
#
# sys.modules[__name__] = Wrapper(sys.modules[__name__])
