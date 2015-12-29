# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
"""
When a window is created, it can be given a specific GL configuration in
order to specify specific GL settings. If no configuration, the default
configuration as provided by the ``get_default`` method is used.

**Usage example**:

  .. code:: python

     from glumpy import app

     config = app.configuration.Configuration()
     config.major_version = 3
     config.minor_version = 2
     config.profile = "core"
     window = app.Window(config=config)
"""
from glumpy.log import log
from glumpy import defaults

# Default configuration
__configuration__ = None



def get_default():
    """
    Return the default configuration.
    """
    global __configuration__

    if __configuration__ is None:
        __configuration__ = Configuration()

    return __configuration__



class Configuration(object):
    """
    GL Configuration settings
    """

    def __init__(self):

        self._red_size            = 8
        self._green_size          = 8
        self._blue_size           = 8
        self._alpha_size          = 8

        self._double_buffer       = defaults.double_buffer()
        self._depth_size          = defaults.depth_size()
        self._stencil_size        = defaults.stencil_size()
        self._samples             = 0

        self._stereo              = defaults.stereo()
        self._srgb                = defaults.srgb()

        self._api                 = defaults.gl_api()
        self._major_version       = defaults.gl_major_version()
        self._minor_version       = defaults.gl_minor_version()
        self._profile             = defaults.gl_profile()


    # ---------------------------------------------------------------- repr ---
    def __repr__(self):
        """
        Configurarion printable description
        """

        s = ""
        s += "Color buffer size:     %d bit(s) (R:%d, G:%d, B:%d, A:%d)\n" % (
            self._red_size + self._green_size + self._blue_size + self._alpha_size,
            self._red_size,
            self._green_size,
            self._blue_size,
            self._alpha_size)
        s += "Depth buffer size:     %d bit(s)\n" % (self._depth_size)
        s += "Stencil buffer size:   %d bit(s)\n" % (self._stencil_size)
        s += "Double buffered:       %d\n" % (self._double_buffer)
        s += "Stereo mode:           %d\n" % (self._stereo)
        s += "sRGB mode:             %d\n" % (self._srgb)
        s += "Anti-aliasing samples: %d\n" % (self._samples)
        s += "GL API:                %s\n" % (self._api)
        s += "GL Version:            %d.%d\n" % (self._major_version,
                                                 self._minor_version)
        s += "GL Profile:            %s" % (self._profile)
        return s



    # ------------------------------------------------------------ red size ---
    @property
    def red_size(self):
        """
        Minimum number of bits for the red channel of the color buffer.
        """
        return self._red_size

    @red_size.setter
    def red_size(self, value):
        self._red_size = value


    # ---------------------------------------------------------- green size ---
    @property
    def green_size(self):
        """
        Minimum number of bits for the blue channel of the color buffer.
        """
        return self._green_size

    @green_size.setter
    def green_size(self, value):
        self._green_size = value

    # ----------------------------------------------------------- blue size ---
    @property
    def blue_size(self):
        """
        Minimum number of bits for the green channel of the color buffer.
        """
        return self._blue_size

    @blue_size.setter
    def blue_size(self, value):
        self._blue_size = value

    # ---------------------------------------------------------- alpha size ---
    @property
    def alpha_size(self):
        """
        Minimum number of bits for the alpha channel of the color buffer.
        """
        return self._alpha_size

    @alpha_size.setter
    def alpha_size(self, value):
        self._alpha_size = value

    # ------------------------------------------------------- double buffer ---
    @property
    def double_buffer(self):
        """
        Whether to use single or double buffered rendering.
        """
        return self._double_buffer

    @double_buffer.setter
    def double_buffer(self, value):
        self._double_buffer = value


    # ---------------------------------------------------------- depth size ---
    @property
    def depth_size(self):
        """
        Minimum number of bits in the depth buffer.
        """
        return self._depth_size

    @depth_size.setter
    def depth_size(self, value):
        self._depth_size = value

    # -------------------------------------------------------- stencil size ---
    @property
    def stencil_size(self):
        """
        Minimum number of bits in the stencil buffer.
        """
        return self._stencil_size

    @stencil_size.setter
    def stencil_size(self, value):
        self._stencil_size = value

    # -------------------------------------------------------------- stereo ---
    @property
    def stereo(self):
        """
        Whether the output is stereo.
        """
        return self._stereo

    @stereo.setter
    def stereo(self, value):
        self._stereo = value

    # ------------------------------------------------------------- samples ---
    @property
    def samples(self):
        """
        Number of samples used around the current pixel for multisample
        anti-aliasing
        """
        return self._samples

    @samples.setter
    def samples(self, value):
        self._samples = value

    # ----------------------------------------------------------------- api ---
    @property
    def api(self):
        """
        OpenGL API
        """
        return self._api

    @api.setter
    def api(self, value):
        self._api = value

    # ------------------------------------------------------- major version ---
    @property
    def major_version(self):
        """
        OpenGL context major version
        """
        return self._major_version

    @major_version.setter
    def major_version(self, value):
        self._major_version = value

    # ------------------------------------------------------- minor version ---
    @property
    def minor_version(self):
        """
        OpenGL context minor version
        """
        return self._minor_version

    @minor_version.setter
    def minor_version(self, value):
        self._minor_version = value

    # ------------------------------------------------------------- profile ---
    @property
    def profile(self):
        """
        OpenGL profile
        """
        return self._profile

    @profile.setter
    def profile(self, value):
        self._profile = value

    # ---------------------------------------------------------------- srgb ---
    @property
    def srgb(self):
        """
        Whether to user sRGB capable visuals.
        """
        return self._srgb

    @srgb.setter
    def srgb(self, value):
        self._srgb = value


# ---------------------------------------------------- gl_get_configuration ---
def gl_get_configuration():
    """
    Read gl configuration independently of backends.
    """

    import ctypes
    import OpenGL.GL as gl

    configuration =  Configuration()
    try:
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)
    except:
        log.warn("Cannot bind framebuffer")

    value = ctypes.c_int()

    try:
        gl.glGetFramebufferAttachmentParameteriv(
            gl.GL_FRAMEBUFFER, gl.GL_FRONT_LEFT,
            gl.GL_FRAMEBUFFER_ATTACHMENT_RED_SIZE, value )
        configuration._red_size = value.value
    except:
        log.warn("Cannot read RED channel size from the framebuffer")
        configuration._red_size = 0

    try:
        gl.glGetFramebufferAttachmentParameteriv(
            gl.GL_FRAMEBUFFER, gl.GL_FRONT_LEFT,
            gl.GL_FRAMEBUFFER_ATTACHMENT_GREEN_SIZE, value )
        configuration._green_size = value.value
    except:
        log.warn("Cannot read GREEN channel size from the framebuffer")
        configuration._green_size = 0

    try:
        gl.glGetFramebufferAttachmentParameteriv(
            gl.GL_FRAMEBUFFER, gl.GL_FRONT_LEFT,
            gl.GL_FRAMEBUFFER_ATTACHMENT_BLUE_SIZE, value )
        configuration._blue_size = value.value
    except:
        log.warn("Cannot read BLUE channel size from the framebuffer")
        configuration._blue_size = 0

    try:
        gl.glGetFramebufferAttachmentParameteriv(
            gl.GL_FRAMEBUFFER, gl.GL_FRONT_LEFT,
            gl.GL_FRAMEBUFFER_ATTACHMENT_ALPHA_SIZE, value )
        configuration._alpha_size = value.value
    except:
        log.warn("Cannot read ALPHA channel size from the framebuffer")
        configuration._alpha_size = 0

    try:
        gl.glGetFramebufferAttachmentParameteriv(
            gl.GL_FRAMEBUFFER, gl.GL_DEPTH,
            gl.GL_FRAMEBUFFER_ATTACHMENT_DEPTH_SIZE, value )
        configuration._depth_size = value.value
    except:
        log.warn("Cannot read DEPTH size from the framebuffer")
        configuration._depth_size = 0

    try:
        gl.glGetFramebufferAttachmentParameteriv(
            gl.GL_FRAMEBUFFER, gl.GL_STENCIL,
            gl.GL_FRAMEBUFFER_ATTACHMENT_STENCIL_SIZE, value )
        configuration._stencil_size = value.value
    except:
        log.warn("Cannot read STENCIL size from the framebuffer")
        configuration._stencil_size = 0

    try:
        gl.glGetFramebufferAttachmentParameteriv(
            gl.GL_FRAMEBUFFER, gl.GL_FRONT_LEFT,
            gl.GL_FRAMEBUFFER_ATTACHMENT_COLOR_ENCODING, value )
        if value.value == gl.GL_LINEAR:
            configuration._srgb = False
        elif value.value == gl.GL_SRGB:
            configuration._srgb = True
    except:
        log.warn("Cannot read sRGB value from the framebuffer")
        configuration._srgb = False


    configuration._stereo        = gl.glGetInteger(gl.GL_STEREO)
    configuration._double_buffer = gl.glGetInteger(gl.GL_DOUBLEBUFFER)
    configuration._samples       = gl.glGetInteger(gl.GL_SAMPLES)

    # Dumb parsing of the GL_VERSION string
    version = gl.glGetString(gl.GL_VERSION).decode()
    version = version.split(" ")[0]
    major,minor = version.split('.')[:2]
    configuration._version = version
    configuration._major_version = int(major)
    configuration._minor_version = int(minor)
    configuration._profile = "unknown"

    return configuration
