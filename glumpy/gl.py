# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
from OpenGL.arrays import numpymodule
numpymodule.NumpyHandler.ERROR_ON_COPY = True

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
