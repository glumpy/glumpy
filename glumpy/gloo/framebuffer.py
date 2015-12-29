# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
"""
A framebuffer is a collection of buffers that can be used as the destination
for rendering. OpenGL has two kinds of framebuffers: the default framebuffer,
which is provided by the OpenGL Context; and user-created framebuffers called
framebuffer objects (FBOs). The buffers for default framebuffers are part of
the context and usually represent a window or display device. The buffers for
FBOs reference images from either textures or render buffers; they are never
directly visible.

Read more on framebuffers on `OpenGL Wiki
<https://www.opengl.org/wiki/Framebuffer>`_

**Example usage**

  .. code:: python

     ...
     texture = np.zeros((512,512,4),np.float32).view(gloo.TextureFloat2D)
     framebuffer = gloo.FrameBuffer(color=[texture])
     ...

     @window.event
     def on_draw(dt):
         window.clear()
         framebuffer.activate()
         quad.draw(gl.GL_TRIANGLE_STRIP)
         framebuffer.deactivate()
"""
import numpy as np
from glumpy import gl
from glumpy.log import log
from glumpy.gloo.globject import GLObject
from glumpy.gloo.texture import Texture2D


class RenderBuffer(GLObject):
    """ Base class for render buffer object.

    :param GLEnum format: Buffer format
    :param int width:     Buffer width (pixels)
    :param int height:    Buffer height (pixel)
    """

    def __init__(self, width=0, height=0, format=None):
        GLObject.__init__(self)
        self._width = width
        self._height = height
        self._target = gl.GL_RENDERBUFFER
        self._format = format
        self._need_resize = True


    @property
    def width(self):
        """ Buffer width (read-only). """

        return self._width


    @property
    def height(self):
        """ Buffer height (read-only). """
        return self._height


    def resize(self, width, height):
        """ Resize the buffer (deferred operation).

        :param int width:  New buffer width (pixels)
        :param int height: New buffer height (pixels)
        """

        if width != self._width or height != self._height:
            self._need_resize = True
            self._width = width
            self._height = height

    def _create(self):
        """ Create buffer on GPU """

        log.debug("GPU: Create render buffer")
        self._handle = gl.glGenRenderbuffers(1)


    def _delete(self):
        """ Delete buffer from GPU """

        log.debug("GPU: Deleting render buffer")
        gl.glDeleteRenderbuffer(self._handle)


    def _activate(self):
        """ Activate buffer on GPU """

        log.debug("GPU: Activate render buffer")
        gl.glBindRenderbuffer(gl.GL_RENDERBUFFER, self._handle)
        if self._need_resize:
            self._resize()
            self._need_resize = False


    def _deactivate(self):
        """ Deactivate buffer on GPU """

        log.debug("GPU: Deactivate render buffer")
        gl.glBindRenderbuffer(gl.GL_RENDERBUFFER, 0)


    def _resize(self):
        """ Buffer resize on GPU """

        # WARNING: width/height should be checked against maximum size
        # maxsize = gl.glGetParameter(gl.GL_MAX_RENDERBUFFER_SIZE)
        log.debug("GPU: Resize render buffer")
        gl.glRenderbufferStorage(self._target, self._format,
                                 self._width, self._height)




class ColorBuffer(RenderBuffer):
    """ Color buffer object.

    :param int width:     Buffer width (pixels)
    :param int height:    Buffer height (pixel)
    :param GLEnum format: Buffer format (default is gl.GL_RGBA)
    """

    def __init__(self, width, height, format=gl.GL_RGBA):
        # if format not in (gl.GL_RGB565, gl.GL_RGBA4, gl.GL_RGB5_A1):
        #     raise ValueError("Format not allowed for color buffer")
        RenderBuffer.__init__(self, width, height, format)





class DepthBuffer(RenderBuffer):
    """ Depth buffer object.

    :param int width:     Buffer width (pixels)
    :param int height:    Buffer height (pixel)
    :param GLEnum format: Buffer format (default is gl.GL_DEPTH_COMPONENT)
    """

    def __init__(self, width, height, format=gl.GL_DEPTH_COMPONENT):
        #if format not in (gl.GL_DEPTH_COMPONENT16,):
        #    raise ValueError("Format not allowed for depth buffer")
        RenderBuffer.__init__(self, width, height, format)



class StencilBuffer(RenderBuffer):
    """ Stencil buffer object

    :param int width:     Buffer width (pixels)
    :param int height:    Buffer height (pixel)
    :param GLEnum format: Buffer format (default is gl.GL_STENCIL_INDEX8)
    """

    def __init__(self, width, height, format=gl.GL_STENCIL_INDEX8):
        # if format not in (gl.GL_STENCIL_INDEX,):
        #     raise ValueError("Format not allowed for color buffer")
        RenderBuffer.__init__(self, width, height, format)




class FrameBuffer(GLObject):
    """ Framebuffer object.

    :param ColorBuffer color:     One or several color buffers or None
    :param DepthBuffer depth:     A depth buffer or None
    :param StencilBuffer stencil: A stencil buffer or None
    """

    def __init__(self, color=None, depth=None, stencil=None):
        """
        """

        GLObject.__init__(self)

        self._width = 0
        self._height = 0
        self._color = None
        self._depth = None
        self._stencil = None
        self._need_attach = True
        self._pending_attachments = []

        if color is not None:
            self.color = color
        if depth is not None:
            self.depth = depth
        if stencil is not None:
            self.stencil = stencil

    @property
    def color(self):
        """ Color buffer attachment(s) (read/write) """

        return self._color


    @color.setter
    def color(self, buffers):
        """ Color buffer attachment(s) (read/write) """

        if not isinstance(buffers,list):
            buffers = [buffers]

        self._color = []

        for i,buffer in enumerate(buffers):
            if self.width != 0 and self.width != buffer.width:
                raise ValueError("Buffer width does not match")
            elif self.height != 0 and self.height != buffer.height:
                raise ValueError("Buffer height does not match")
            self._width = buffer.width
            self._height = buffer.height

            target = gl.GL_COLOR_ATTACHMENT0+i
            self._color.append(buffer)

            if isinstance(buffer, (ColorBuffer, Texture2D)) or buffer is None:
                self._pending_attachments.append((target, buffer))
            else:
                raise ValueError(
                    "Buffer must be a ColorBuffer, Texture2D or None")
        self._need_attach = True


    @property
    def depth(self):
        """ Depth buffer attachment (read/write) """

        return self._depth


    @depth.setter
    def depth(self, buffer):
        """ Depth buffer attachment (read/write) """

        if self.width != 0 and self.width != buffer.width:
            raise ValueError("Buffer width does not match")
        elif self.height != 0 and self.height != buffer.height:
            raise ValueError("Buffer height does not match")
        self._width = buffer.width
        self._height = buffer.height

        target = gl.GL_DEPTH_ATTACHMENT
        self._depth = buffer
        if isinstance(buffer, (DepthBuffer, Texture2D)) or buffer is None:
            self._pending_attachments.append((target, buffer))
        else:
            raise ValueError(
                "Buffer must be a DepthBuffer, Texture2D or None")
        self._need_attach = True


    @property
    def stencil(self):
        """ Stencil buffer attachment (read/write) """

        return self._stencil


    @stencil.setter
    def stencil(self, buffer):
        """ Stencil buffer attachment (read/write) """

        if self.width != 0 and self.width != buffer.width:
            raise ValueError("Buffer width does not match")
        elif self.height != 0 and self.height != buffer.height:
            raise ValueError("Buffer height does not match")
        self._width = buffer.width
        self._height = buffer.height

        target = gl.GL_STENCIL_ATTACHMENT
        self._stencil = buffer
        if isinstance(buffer, StencilBuffer) or buffer is None:
            self._pending_attachments.append((target, buffer))
        else:
            raise ValueError(
                "Buffer must be a StencilBuffer, Texture2D or None")
        self._need_attach = True


    @property
    def width(self):
        """ Buffer width (read only, pixels) """

        return self._width


    @property
    def height(self):
        """ Buffer height (read only, pixels) """

        return self._height


    def resize(self, width, height):
        """ Resize the buffer (deferred operation).

        This method will also resize any attached buffers.

        :param int width:  New buffer width (pixels)
        :param int height: New buffer height (pixels)
        """

        self._width = width
        self._height = height

        for i, buffer in enumerate(self.color):
            if isinstance(buffer, ColorBuffer):
                buffer.resize(width, height)
            elif isinstance(buffer, Texture2D):
                newbuffer = np.resize(buffer, (height,width,buffer.shape[2]))
                newbuffer = newbuffer.view(buffer.__class__)
                self.color[i] = newbuffer
                buffer.delete()

                target = gl.GL_COLOR_ATTACHMENT0+i
                self._pending_attachments.append((target, self.color[i]))
                self._need_attach = True

        if isinstance(self.depth, DepthBuffer):
            self.depth.resize(width, height)
        elif isinstance(self.depth, Texture2D):
            depth = np.resize(self.depth, (height,width, self.depth.shape[2]))
            depth = depth.view(self.depth.__class__)
            self.depth.delete()
            self.depth = depth

            target = gl.GL_DEPTH_ATTACHMENT
            self._pending_attachments.append((target, self.depth))
            self._need_attach = True

        if isinstance(self.stencil, StencilBuffer):
            self.stencil.resize(width, height)
        elif isinstance(self.stencil, Texture2D):
            stencil = np.resize(self.stencil, (height,width, self.stencil.shape[2]))
            stencil = stencil.view(self.stencil.__class__)
            self.stencil.delete()
            self.stencil = stencil

            target = gl.GL_STENCIL_ATTACHMENT
            self._pending_attachments.append((target, self.stencil))
            self._need_attach = True


    def _create(self):
        """ Create framebuffer on GPU """

        log.debug("GPU: Create framebuffer")
        self._handle = gl.glGenFramebuffers(1)


    def _delete(self):
        """ Delete buffer from GPU """

        log.debug("GPU: Delete framebuffer")
        gl.glDeleteFramebuffer(self._handle)


    def _activate(self):
        """ Activate framebuffer on GPU """

        log.debug("GPU: Activate render framebuffer")
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self._handle)

        if self._need_attach:
            self._attach()
            self._need_attach = False
        attachments = [gl.GL_COLOR_ATTACHMENT0+i for i in range(len(self.color))]
        gl.glDrawBuffers(np.array(attachments,dtype=np.uint32))


    def _deactivate(self):
        """ Deactivate framebuffer on GPU """

        log.debug("GPU: Deactivate render framebuffer")
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)
        # gl.glDrawBuffers([gl.GL_COLOR_ATTACHMENT0])


    def _attach(self):
        """ Attach render buffers to framebuffer """

        log.debug("GPU: Attach render buffers")
        while self._pending_attachments:
            attachment, buffer = self._pending_attachments.pop(0)
            if buffer is None:
                gl.glFramebufferRenderbuffer(gl.GL_FRAMEBUFFER, attachment,
                                             gl.GL_RENDERBUFFER, 0)
            elif isinstance(buffer, RenderBuffer):
                buffer.activate()
                gl.glFramebufferRenderbuffer(gl.GL_FRAMEBUFFER, attachment,
                                             gl.GL_RENDERBUFFER, buffer.handle)
                buffer.deactivate()
            elif isinstance(buffer, Texture2D):
                buffer.activate()
                # INFO: 0 is for mipmap level 0 (default) of the texture
                gl.glFramebufferTexture2D(gl.GL_FRAMEBUFFER, attachment,
                                          buffer.target, buffer.handle, 0)
                buffer.deactivate()
            else:
                raise ValueError("Invalid attachment")


        res = gl.glCheckFramebufferStatus(gl.GL_FRAMEBUFFER)
        if res == gl.GL_FRAMEBUFFER_COMPLETE:
            pass
        elif res == 0:
            raise RuntimeError('Target not equal to GL_FRAMEBUFFER')
        elif res == gl.GL_FRAMEBUFFER_INCOMPLETE_ATTACHMENT:
            raise RuntimeError(
                'FrameBuffer attachments are incomplete.')
        elif res == gl.GL_FRAMEBUFFER_INCOMPLETE_MISSING_ATTACHMENT:
            raise RuntimeError(
                'No valid attachments in the FrameBuffer.')
        elif res == gl.GL_FRAMEBUFFER_INCOMPLETE_DIMENSIONS:
            raise RuntimeError(
                'attachments do not have the same width and height.')
        elif res == gl.GL_FRAMEBUFFER_INCOMPLETE_FORMATS:
            raise RuntimeError('Internal format of attachment '
                               'is not renderable.')
        elif res == gl.GL_FRAMEBUFFER_UNSUPPORTED:
            raise RuntimeError('Combination of internal formats used '
                               'by attachments is not supported.')
