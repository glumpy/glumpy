# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
"""
All default parameters and objects.
"""

# ------------------------------------------------------------------ Parser ---
def get_default_parser():
    """ Default command line argument parser """
    from glumpy.app.parser import get_default
    return get_default()

def parser():
    """ Default command line argument parser """
    return get_default_parser()


# ------------------------------------------------------------------- Clock ---
def get_default_clock():
    """ Default clock """
    from glumpy.app.clock import get_default
    return get_default()

def clock():
    """ Default clock """
    return get_default_clock()


# ----------------------------------------------------------- Configuration ---
def get_default_configuration():
    """ Default configuration """
    from glumpy.app.configuration import get_default
    return get_default()

def configuration():
    """ Default command line argument parser """
    return get_default_configuration()


# ------------------------------------------------------------ Window width ---
__width__ = 512

def get_default_width():
    """ Default window width """
    return __width__

def width():
    """ Default window width """
    return get_default_width()


# ----------------------------------------------------------- Window height ---
__height__ = 512

def get_default_height():
    """ Default window height """
    return __height__

def height():
    """ Default window height """
    return get_default_height()


# ------------------------------------------------------- Window x position ---
__x__ = 0

def get_default_x():
    """ Default window x position """
    return __x__

def x():
    """ Default window width """
    return get_default_x()


# ------------------------------------------------------- Window y position ---
__y__ = 0

def get_default_y():
    """ Default window y position """
    return __y__

def y():
    """ Default window width """
    return get_default_y()


# --------------------------------------------------------------- Framerate ---
__framerate__ = 60.0

def get_default_framerate():
    """ Default framerate """
    return __framerate__

def framerate():
    """ Default framerate """
    return get_default_framerate()


# ------------------------------------------------------------------- vsync ---
__vsync__ = False

def get_default_vsync():
    """ Default vsync """
    return __vsync__

def vsync():
    """ Default vsync """
    return get_default_vsync()


# -------------------------------------------------------------------- srgb ---
__srgb__ = False

def get_default_srgb():
    """ Default srgb """
    return __srgb__

def srgb():
    """ Default srgb """
    return get_default_srgb()


# ------------------------------------------------------------------ stereo ---
__stereo__ = False

def get_default_stereo():
    """ Default stereo """
    return __stereo__

def stereo():
    """ Default stereo """
    return get_default_stereo()


# ----------------------------------------------------------- double buffer ---
__double_buffer__ = True

def get_default_double_buffer():
    """ Default double buffer mode """
    return __double_buffer__

def double_buffer():
    """ Default double buffer """
    return get_default_double_buffer()


# -------------------------------------------------------------- depth_size ---
__depth_size__ = 24

def get_default_depth_size():
    """ Default depth size """
    return __depth_size__

def depth_size():
    """ Default depth size """
    return get_default_depth_size()


# ------------------------------------------------------------ stencil size ---
__stencil_size__ = 0

def get_default_stencil_size():
    """ Default stencil size """
    return __stencil_size__

def stencil_size():
    """ Default stencil size """
    return get_default_stencil_size()


# -------------------------------------------------------------- GL Version ---
__gl_major_version__ = 2
__gl_minor_version__ = 1

def get_default_gl_version():
    """ Default GL version """
    return "%d.%d" % (__gl_major_version__,__gl_minor_version__)

def gl_version():
    """ Default GL version """
    return get_default_gl_version()

def get_default_gl_major_version():
    """ Default GL major version """
    return __gl_major_version__

def gl_major_version():
    """ Default GL major version """
    return get_default_gl_major_version()

def get_default_gl_minor_version():
    """ Default GL minor version """
    return __gl_minor_version__

def gl_minor_version():
    """ Default GL minor version """
    return get_default_gl_minor_version()


# ------------------------------------------------------------------ GL API ---
__gl_api__ = "GL"

def get_default_gl_api():
    """ Default GL API """
    return __gl_api__

def gl_api():
    """ Default GL API """
    return get_default_gl_api()


# -------------------------------------------------------------- GL profile ---
__gl_profile__ = "none"

def get_default_gl_profile():
    """ Default GL profile """
    return __gl_profile__

def gl_profile():
    """ Default GL profile """
    return get_default_gl_profile()


# ----------------------------------------------------------------- Backend ---
__backend__ = "glfw"

def get_default_backend():
    """ Default backend """
    return __backend__

def backend():
    """ Default backend """
    return get_default_backend()
