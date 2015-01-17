#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np

from glumpy import gl
from glumpy.log import log
from glumpy.gloo.gpudata import GPUData
from glumpy.gloo.globject import GLObject


class Buffer(GPUData,GLObject):
    """
    Generic GPU buffer.

    A generic buffer is an interface used to upload data to a GPU array buffer
    (gl.GL_ARRAY_BUFFER or gl.GL_ELEMENT_ARRAY_BUFFER).
    """

    def __init__(self, target, usage=gl.GL_DYNAMIC_DRAW):
        GLObject.__init__(self)
        self._target = target
        self._usage = usage


    @property
    def need_update(self):
        """ Whether object needs to be updated """

        return self.pending_data is not None


    def _create(self):
        """ Create buffer on GPU """

        self._handle = gl.glGenBuffers(1)
        self._activate()
        log.debug("GPU: Creating buffer (id=%d)" % self._id)
        gl.glBufferData(self._target, self.nbytes, None, self._usage)
        self._deactivate()


    def _delete(self):
        """ Delete buffer from GPU """

        if self._handle > -1:
            gl.glDeleteBuffers(1, [self._handle])


    def _activate(self):
        """ Bind the buffer to some target """

        log.debug("GPU: Activating buffer (id=%d)" % self._id)
        gl.glBindBuffer(self._target, self._handle)


    def _deactivate(self):
        """ Unbind the current bound buffer """

        log.debug("GPU: Deactivating buffer (id=%d)" % self._id)
        gl.glBindBuffer(self._target, 0)


    def _update(self):
        """ Upload all pending data to GPU. """

        if self.pending_data:
            start, stop = self.pending_data
            offset, nbytes = start, stop-start
            # offset, nbytes = self.pending_data
            data = self.ravel().view(np.ubyte)[offset:offset+nbytes]
            gl.glBufferSubData(self.target, offset, nbytes, data)
        self._pending_data = None
        self._need_update = False



class VertexBuffer(Buffer):
    """ Buffer for vertex attribute data """

    def __init__(self, usage=gl.GL_DYNAMIC_DRAW):
        Buffer.__init__(self, gl.GL_ARRAY_BUFFER, usage)


class IndexBuffer(Buffer):
    """ Buffer for index data """

    def __init__(self, usage=gl.GL_DYNAMIC_DRAW):
        Buffer.__init__(self, gl.GL_ELEMENT_ARRAY_BUFFER, usage)
