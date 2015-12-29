# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
"""
A texture is an OpenGL Object that contains one or more images that all
have the same image format. A texture can be used in two ways. It can be the
source of a texture access from a Shader, or it can be used as a render target.

Read more on framebuffers on `OpenGL Wiki <https://www.opengl.org/wiki/Texture>`_

**Example usage**:

  .. code::

     ...
    fragment = '''
        uniform sampler2D texture;
        varying vec2 v_texcoord;
        void main()
        {
           gl_FragColor = texture2D(texture, v_texcoord);
        } '''

    ...
    quad = gloo.Program(vertex, fragment, count=4)
    quad['texture'] = data.get('lena.png')
    ...
"""

import numpy as np
from glumpy import gl
from glumpy.log import log
from glumpy.gloo.gpudata import GPUData
from glumpy.gloo.globject import GLObject


class Texture(GPUData,GLObject):
    """ Generic texture """

    _cpu_formats = { 1: gl.GL_RED,
                     2: gl.GL_RG,
                     3: gl.GL_RGB,
                     4: gl.GL_RGBA }

    _gpu_formats = { 1: gl.GL_RED,
                     2: gl.GL_RG,
                     3: gl.GL_RGB,
                     4: gl.GL_RGBA }

    _gpu_float_formats = { 1: gl.GL_R32F,
                           2: gl.GL_RG32F,
                           3: gl.GL_RGB32F,
                           4: gl.GL_RGBA32F }

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
        self._cpu_format = None
        self._gpu_format = None

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
    def cpu_format(self):
        """
        Texture CPU format (read/write).
       
        Depending on integer or float textures, one of:

        * gl.GL_RED  / gl.GLR32F
        * gl.GL_RG   / gl.GL_RG32F
        * gl.GL_RGB  / gl.GL_RGB32F
        * gl.GL_RGBA / gl.GL_RGBA32F
        """

        return self._cpu_format

    @property
    def gpu_format(self):
        """ 
        Texture GPU format (read/write).

        Depending on integer or float textures, one of:

        * gl.GL_RED  / gl.GLR32F
        * gl.GL_RG   / gl.GL_RG32F
        * gl.GL_RGB  / gl.GL_RGB32F
        * gl.GL_RGBA / gl.GL_RGBA32F
        """

        return self._gpu_format


    @gpu_format.setter
    def gpu_format(self, value):
        """ Texture GPU format. """

        self._gpu_format = value
        self._need_setup = True


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
        gl.glTexParameterf(self.target, gl.GL_TEXTURE_WRAP_R, gl.GL_CLAMP_TO_EDGE)
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
            gl.glDeleteTextures(np.array([self.handle], dtype=np.uint32))




class Texture1D(Texture):
    """
    One dimensional texture.
    """

    def __init__(self):
        Texture.__init__(self, gl.GL_TEXTURE_1D)
        self.shape = self._check_shape(self.shape, 1)
        self._cpu_format = Texture._cpu_formats[self.shape[-1]]
        self._gpu_format = Texture._gpu_formats[self.shape[-1]]


    @property
    def width(self):
        """ 
        Texture width
        """

        return self.shape[0]

    
#    def _create(self):
#        Texture._create(self)
#        log.debug("GPU: Resizing texture(%s)"% (self.width))
#        gl.glBindTexture(self.target, self._handle)
#        gl.glTexImage1D(self.target, 0, self.format, self.width,
#                        0, self.format, self.gtype, None)

    def _setup(self):
        """ Setup texture on GPU """

        Texture._setup(self)
        gl.glBindTexture(self.target, self._handle)
        gl.glTexImage1D(self.target, 0, self._gpu_format, self.width,
                        0, self._cpu_format, self.gtype, None)
        self._need_setup = False

    def _update(self):

        log.debug("GPU: Updating texture")
        if self.pending_data:
            start, stop = self.pending_data
            offset, nbytes = start, stop-start
            itemsize = self.strides[0]
            x = offset // itemsize
            width = nbytes//itemsize
            gl.glTexSubImage1D(self.target, 0, x, width, self._cpu_format, self.gtype, self)

            # x,width = self.pending_data
            # itemsize = self.strides[0]
            # x /= itemsize
            # width /= itemsize
            # gl.glTexSubImage1D(self.target, 0, x, width, self._cpu_format, self.gtype, self)
        self._pending_data = None
        self._need_update = False


class TextureFloat1D(Texture1D):
    """
    One dimensional float texture.
    """

    def __init__(self):
        Texture1D.__init__(self)
        self._gpu_format = Texture._gpu_float_formats[self.shape[-1]]



class Texture2D(Texture):
    """ 2D texture """

    def __init__(self):
        Texture.__init__(self, gl.GL_TEXTURE_2D)
        self.shape = self._check_shape(self.shape, 2)
        self._cpu_format = Texture._cpu_formats[self.shape[-1]]
        self._gpu_format = Texture._gpu_formats[self.shape[-1]]

    @property
    def width(self):
        """ Texture width """

        return self.shape[1]


    @property
    def height(self):
        """ Texture height """

        return self.shape[0]


    # def _create(self):
    #     """ Create texture on GPU """

    #     Texture._create(self)
    #     log.debug("GPU: Resizing texture(%sx%s)"% (self.width,self.height))
    #     gl.glBindTexture(self.target, self._handle)
    #     gl.glTexImage2D(self.target, 0, self.format, self.width, self.height,
    #                     0, self.format, self.gtype, None)
    #     """
    #     if self.format == gl.GL_RED:
    #         gl.glTexImage2D(self.target, 0, gl.GL_R32F, self.width, self.height,
    #                         0, self.format, self.gtype, None)

    #     elif self.format == gl.GL_RG:
    #         gl.glTexImage2D(self.target, 0, gl.GL_RG32F, self.width, self.height,
    #                         0, self.format, self.gtype, None)
    #     elif self.format == gl.GL_RGB:
    #         gl.glTexImage2D(self.target, 0, gl.GL_RGB32F, self.width, self.height,
    #                         0, self.format, self.gtype, None)
    #     elif self.format == gl.GL_RGBA:
    #         gl.glTexImage2D(self.target, 0, gl.GL_RGBA32F, self.width, self.height,
    #                         0, self.format, self.gtype, None)
    #     """

    def _setup(self):
        """ Setup texture on GPU """

        Texture._setup(self)
        gl.glBindTexture(self.target, self._handle)
        gl.glTexImage2D(self.target, 0, self._gpu_format, self.width, self.height,
                        0, self._cpu_format, self.gtype, None)
        self._need_setup = False


    def _update(self):
        """ Update texture on GPU """

        if self.pending_data:
            log.debug("GPU: Updating texture")

            start, stop = self.pending_data
            offset, nbytes = start, stop-start

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
                               self._cpu_format, self.gtype, self)
            gl.glBindTexture(self._target, self.handle)

        self._pending_data = None
        self._need_update = False



class TextureFloat2D(Texture2D):
    """ 2D float texture """

    def __init__(self):
        Texture2D.__init__(self)
        self._gpu_format = Texture._gpu_float_formats[self.shape[-1]]


class DepthTexture(Texture2D):
    """ Depth texture """

    def __init__(self):
        Texture2D.__init__(self)
        self._cpu_format = gl.GL_DEPTH_COMPONENT
        self._gpu_format = gl.GL_DEPTH_COMPONENT



class TextureCube(Texture):
    """ Cube texture """

    def __init__(self):

        Texture.__init__(self, gl.GL_TEXTURE_CUBE_MAP)
        if self.shape[0] != 6:
            error = "Texture cube require arrays first dimension to be 6"
            log.error(error)
            raise RuntimeError(error)

        self.shape = [6] + list(self._check_shape(self.shape[1:], 2))
        self._cpu_format = Texture._cpu_formats[self.shape[-1]]
        self._gpu_format = Texture._gpu_formats[self.shape[-1]]

    @property
    def width(self):
        """ Texture width """

        return self.shape[2]


    @property
    def height(self):
        """ Texture height """

        return self.shape[1]


    def _setup(self):
        """ Setup texture on GPU """

        Texture._setup(self)
        gl.glEnable(gl.GL_TEXTURE_CUBE_MAP)
        gl.glBindTexture(self.target, self._handle)
        targets = [ gl.GL_TEXTURE_CUBE_MAP_POSITIVE_X,
                    gl.GL_TEXTURE_CUBE_MAP_NEGATIVE_X,
                    gl.GL_TEXTURE_CUBE_MAP_POSITIVE_Y,
                    gl.GL_TEXTURE_CUBE_MAP_NEGATIVE_Y,
                    gl.GL_TEXTURE_CUBE_MAP_POSITIVE_Z,
                    gl.GL_TEXTURE_CUBE_MAP_NEGATIVE_Z ]
        for i,target in enumerate(targets):
            gl.glTexImage2D(target, 0, self._gpu_format, self.width, self.height,
                            0, self._cpu_format, self.gtype, None)
        self._need_setup = False


    def _update(self):
        log.debug("GPU: Updating texture cube")

        if self.need_update:
            gl.glEnable(gl.GL_TEXTURE_CUBE_MAP)
            gl.glBindTexture(self.target, self.handle)

            targets = [ gl.GL_TEXTURE_CUBE_MAP_POSITIVE_X,
                        gl.GL_TEXTURE_CUBE_MAP_NEGATIVE_X,
                        gl.GL_TEXTURE_CUBE_MAP_POSITIVE_Y,
                        gl.GL_TEXTURE_CUBE_MAP_NEGATIVE_Y,
                        gl.GL_TEXTURE_CUBE_MAP_POSITIVE_Z,
                        gl.GL_TEXTURE_CUBE_MAP_NEGATIVE_Z ]

            for i,target in enumerate(targets):
                face = self[i]
                pending = self.pending_data
                extents = face._extents
                if pending is None:         continue
                if pending[1] < extents[0]: continue
                if pending[0] > extents[1]: continue
                start = max(extents[0], pending[0]) - extents[0]
                stop = min(extents[1], pending[1]) - extents[0]
                offset,nbytes = start, stop-start
                itemsize = face.strides[1]
                offset /= itemsize
                nbytes /= itemsize
                nbytes += offset % self.width
                offset -= offset % self.width
                nbytes += (self.width - ((offset + nbytes) % self.width)) % self.width
                x = 0
                y = offset // self.width
                width = self.width
                height = nbytes // self.width
                gl.glTexSubImage2D(target, 0, x, y, width, height,
                                   self._cpu_format, self.gtype, face)

        self._pending_data = None
        self._need_update = False

    def _activate(self):
        """ Activate texture on GPU """

        log.debug("GPU: Activate texture cube")
        gl.glEnable(gl.GL_TEXTURE_CUBE_MAP)
        gl.glBindTexture(self.target, self._handle)
        if self._need_setup:
            self._setup()


    def _deactivate(self):
        """ Deactivate texture on GPU """

        log.debug("GPU: Deactivate texture cube")
        gl.glBindTexture(self._target, 0)
        gl.glDisable(gl.GL_TEXTURE_CUBE_MAP)
