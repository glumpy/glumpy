# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
"""
Vertex Array objects are OpenGL objects that store all of the state needed
to supply vertex data. Only available from GL > 3.2.

Read more on buffer objects on `OpenGL Wiki
<https://www.opengl.org/wiki/Vertex_Specification>`_

**Example usage**:

  .. code:: python

     dtype = [("position", np.float32, 3),
              ("color",    np.float32, 4)]
     V = np.zeros(4,dtype).view(gloo.VertexArray)
"""
import numpy as np

from glumpy import gl
from glumpy.log import log
from glumpy.gloo.gpudata import GPUData
from glumpy.gloo.globject import GLObject
from glumpy.gloo.buffer import VertexBuffer

class VertexArray(GPUData,GLObject):
    """
    Vertex array.

    A vertex array is an interface used to specify vertex data structure.
    """

    def __init__(self, usage=gl.GL_DYNAMIC_DRAW):
        GLObject.__init__(self)
        self._target = gl.GL_ARRAY_BUFFER
        self._buffer = self.view(VertexBuffer)
        self._buffer.__init__(usage)


    @property
    def need_update(self):
        """ Whether object needs to be updated """

        return self._buffer.need_update


    def _update(self):
        """ Upload all pending data to GPU. """

        self._buffer._update()

    
    def _create(self):
        """ Create vertex array on GPU """

        self._handle = gl.glGenVertexArrays(1)
        log.debug("GPU: Creating vertex array (id=%d)" % self._id)
        self._deactivate()
        self._buffer._create()

        
    def _delete(self):
        """ Delete vertex array from GPU """

        if self._handle > -1:
            self._buffer._delete()
            gl.glDeleteVertexArrays(1, np.array([self._handle]))


    def _activate(self):
        """ Bind the array """

        log.debug("GPU: Activating array (id=%d)" % self._id)
        gl.glBindVertexArray(self._handle)
        self._buffer._activate()
        

    def _deactivate(self):
        """ Unbind the current bound array """

        self._buffer._deactivate()
        log.debug("GPU: Deactivating array (id=%d)" % self._id)
        gl.glBindVertexArray(0)
