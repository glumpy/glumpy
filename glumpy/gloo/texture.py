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


class Texture(GPUData,GLObject):
    """ Generic texture """

    _formats = { # 1: gl.GL_LUMINANCE,
                 # 2: gl.GL_LUMINANCE_ALPHA,
                 1: gl.GL_RED,
                 2: gl.GL_RG,
                 3: gl.GL_RGB,
                 4: gl.GL_RGBA }

    _gtypes = { np.dtype(np.int8):    gl.GL_BYTE,
                np.dtype(np.uint8):   gl.GL_UNSIGNED_BYTE,
                np.dtype(np.int16):   gl.GL_SHORT,
                np.dtype(np.uint16):  gl.GL_UNSIGNED_SHORT,
                np.dtype(np.int32):   gl.GL_INT,
                np.dtype(np.uint32):  gl.GL_UNSIGNED_INT,
                np.dtype(np.float32): gl.GL_FLOAT }

    def __init__(self, target):
        GLObject.__init__(self)
        self._target = target
        # self._interpolation = gl.GL_LINEAR, gl.GL_LINEAR
        self._interpolation = gl.GL_NEAREST, gl.GL_NEAREST
        self._wrapping = gl.GL_CLAMP_TO_EDGE

    def _check_shape(self, shape, ndims):
        """ Check and normalize shape. """

        if len(shape) < ndims:
            raise ValueError("Too few dimensions for texture")
        elif len(shape) > ndims+1:
            raise ValueError("Too many dimensions for texture")
        elif len(shape) == ndims:
            shape = list(shape) + [1,]
        elif len(shape) == ndims+1:
            if shape[-1] > 4:
                raise ValueError("Too many channels for texture")
        return shape


    @property
    def need_update(self):
        """ Whether object needs to be updated """

        return self.pending_data is not None


    @property
    def format(self):
        """ Texture format. """

        return Texture._formats[self.shape[-1]]


    @property
    def gtype(self):
        if self.dtype in Texture._gtypes.keys():
            return Texture._gtypes[self.dtype]
        else:
            raise TypeError("No available GL type equivalent")

    @property
    def wrapping(self):
        """ Texture wrapping mode """

        return self._wrapping

    @wrapping.setter
    def wrapping(self, value):
        """ Texture wrapping mode """

        self._wrapping = value
        self._need_setup = True

    @property
    def interpolation(self):
        """ Texture interpolation for minification and magnification. """

        return self._interpolation

    @interpolation.setter
    def interpolation(self, value):
        """ Texture interpolation for minication and magnification. """

        if isinstance(value, (list,tuple)):
            self._interpolation = value
        else:
            self._interpolation = value,value
        self._need_setup = True


    def _setup(self):
        """ Setup texture on GPU """

        min_filter, mag_filter = self._interpolation
        wrapping = self._wrapping

        gl.glTexParameterf(self.target, gl.GL_TEXTURE_MIN_FILTER, min_filter)
        gl.glTexParameterf(self.target, gl.GL_TEXTURE_MAG_FILTER, mag_filter)
        gl.glTexParameterf(self.target, gl.GL_TEXTURE_WRAP_S, wrapping)
        gl.glTexParameterf(self.target, gl.GL_TEXTURE_WRAP_T, wrapping)
        self._need_setup = False


    def _activate(self):
        """ Activate texture on GPU """

        log.debug("GPU: Activate texture")
        gl.glBindTexture(self.target, self._handle)
        if self._need_setup:
            self._setup()


    def _deactivate(self):
        """ Deactivate texture on GPU """

        log.debug("GPU: Deactivate texture")
        gl.glBindTexture(self._target, 0)


    def _create(self):
        """ Create texture on GPU """

        log.debug("GPU: Creating texture")
        self._handle = gl.glGenTextures(1)

    def _delete(self):
        """ Delete texture from GPU """

        log.debug("GPU: Deleting texture")
        if self.handle > -1:
            gl.glDeleteTextures([self.handle])




class Texture1D(Texture):
    """ 1D Texture """

    def __init__(self):
        Texture.__init__(self, gl.GL_TEXTURE_1D)
        self.shape = self._check_shape(self.shape, 1)

    @property
    def width(self):
        return self.shape[0]

    def _create(self):
        Texture._create(self)

        log.debug("GPU: Resizing texture(%s)"% (self.width))
        gl.glBindTexture(self.target, self._handle)
        gl.glTexImage1D(self.target, 0, self.format, self.width,
                        0, self.format, self.gtype, None)

    def _update(self):

        log.debug("GPU: Updating texture")
        if self.pending_data:
            x,width = self.pending_data
            itemsize = self.strides[0]
            x /= itemsize
            width /= itemsize
            gl.glTexSubImage1D(self.target, 0, x, width, self.format, self.gtype, self)
        self._pending_data = None
        self._need_update = False



class Texture2D(Texture):
    """ 2D Texture """

    def __init__(self):
        Texture.__init__(self, gl.GL_TEXTURE_2D)
        self.shape = self._check_shape(self.shape, 2)

    @property
    def width(self):
        """ Texture width """

        return self.shape[1]


    @property
    def height(self):
        """ Texture height """

        return self.shape[0]


    def _create(self):
        """ Create texture on GPU """

        Texture._create(self)
        log.debug("GPU: Resizing texture(%sx%s)"% (self.width,self.height))
        gl.glBindTexture(self.target, self._handle)
        #        gl.glTexImage2D(self.target, 0, self.format, self.width, self.height,
        #                        0, self.format, self.gtype, None)
        if self.format == gl.GL_RED:
            gl.glTexImage2D(self.target, 0, gl.GL_R32F, self.width, self.height,
                            0, self.format, self.gtype, None)

        elif self.format == gl.GL_RG:
            gl.glTexImage2D(self.target, 0, gl.GL_RG32F, self.width, self.height,
                            0, self.format, self.gtype, None)
        elif self.format == gl.GL_RGB:
            gl.glTexImage2D(self.target, 0, gl.GL_RGB32F, self.width, self.height,
                            0, self.format, self.gtype, None)
        elif self.format == gl.GL_RGBA:
            gl.glTexImage2D(self.target, 0, gl.GL_RGBA32F, self.width, self.height,
                            0, self.format, self.gtype, None)

    def _update(self):
        """ Update texture on GPU """

        if self.pending_data:
            log.debug("GPU: Updating texture")

            offset, nbytes = self.pending_data

            itemsize = self.strides[1]
            offset /= itemsize
            nbytes /= itemsize

            nbytes += offset % self.width
            offset -= offset % self.width
            nbytes += (self.width - ((offset + nbytes) % self.width)) % self.width

            x = 0
            y = offset // self.width
            width = self.width
            height = nbytes // self.width
            gl.glBindTexture(self._target, self.handle)
            gl.glTexSubImage2D(self.target, 0, x, y, width, height,
                               self.format, self.gtype, self)
            gl.glBindTexture(self._target, self.handle)

        self._pending_data = None
        self._need_update = False
