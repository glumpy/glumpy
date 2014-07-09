# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
"""
"""
import os
import re
import sys
import logging
import importlib

from glumpy import gl
from glumpy.log import log
from glumpy.app import parser
from glumpy.app import configuration
from glumpy.app import clock as _clock
from glumpy.app.window import backends
from glumpy.app.window.viewport import Viewport


# Default clock
__clock__ = None

# Active windows
__windows__ = []

# Current backend
__backend__ = None





# --------------------------------------------------------------------- fps ---
def fps():
    """
    Get FPS from the default clock.
    """
    return __clock__.get_fps()


# --------------------------------------------------------------------- use ---
def use(backend, api=None, major=None, minor=None, profile=None):
    """ Select a specific backend

    Parameters
    ----------

    backend : ['osxglut', 'pyglet', 'glfw', 'sdl', 'sdl2', 'pyside']
        Graphical toolkit to use

    api : ['GL'|'ES']
        OpenGL API to use

    major : int
        OpenGL major version to use

    minor : int
        OpenGL minor version to use

    profile : ['compatibility'|'core']
        OpenGL profile to use

    Note
    ----
    A shortened version is available with the following syntax:

    use("backend (api major.minor profile)")

    For example, `use("glfw (GL 3.3 core)")`
    """

    global __backend__

    # Parse options (in backend name, see note above)
    exp = """(?P<backend>\w+)?
             (.*\(
             (.*(?P<api>GL|ES))?
             (.*(?P<major>[1234])\.(?P<minor>[012345]))?
             (.*(?P<profile>compatibility|core))?.*\))?"""
    r = re.search(exp, backend, re.IGNORECASE | re.VERBOSE)
    _backend = r.group('backend') or "glfw"
    _api     = r.group('api') or "GL"
    _major   = int(r.group('major') or "2")
    _minor   = int(r.group('minor') or "1")
    _profile = r.group('profile') or ""

    # Arguments take precedence over shortened options
    backend = _backend
    api     = api or _api
    major   = major or _major
    minor   = minor or _minor
    profile = profile or _profile

    config = configuration.get_default()
    config.api = api
    config.major_version = major
    config.minor_version = minor
    config.profile = profile

    if backend not in backends.__backends__:
        log.critical("Unknown backend (%s)" % backend)
        log.cirtical("Available backends are: %s", str(backends.__backends__))
        sys.exit(0)

    # BUG: For some reason, the import module changes the working directory
    #      We save it beforehand and restore it just after
    workdir = os.getcwd()
    name = "glumpy.app.window.backends.backend_" + backend
    importlib.import_module(name)
    backend = sys.modules[name]
    os.chdir(workdir)

    # Check availability
    if backend.available():
        __backend__ = backend
        return backend
    else:
        log.warning("Backend (%s) not available" % backend)
        return None


# ----------------------------------------------------------------- Window ---
class Window(object):
    """
    Abstract Window

    This class is responsible for finding a suitable backend and parsing
    arguments.
    """

    def __new__(cls, *args, **kwargs):
        global __backend__

        all = list(backends.__backends__)
        options = parser.get_options()

        # No backend was specified
        # Check for command line argument then pick a default one if possible
        if __backend__ is None:
            if options.backend != all[0]:
                all = [options.backend,] + all
            for name in all:
                backend = use(name)
                if backend and backend.available():
                    __backend__ = backend
                    break
            # No backend available, there's nothing we can do
            if __backend__ is None:
                log.critical("No suitable backend found")
                raise NotImplementedError

        # Get configuration
        config = configuration.get_default()
        kwargs['config'] = kwargs.get('config', config)

        # Get command line size
        if options.size:
            size = options.size.split(",")
            kwargs['width'] = int(size[0])
            kwargs['height'] = int(size[1])
        else:
            kwargs['width']  = kwargs.get('width', 512)
            kwargs['height'] = kwargs.get('height', 512)

        # Get command line position
        if options.position:
            position = options.position.split(",")
            #kwargs['x'] = kwargs.get('x', int(position[0]))
            #kwargs['y'] = kwargs.get('y', int(position[1]))
        else:
            pass
            #kwargs['x'] = kwargs.get('x', 0)
            #kwargs['y'] = kwargs.get('y', 0)


        # Create the backend window
        window = __backend__.Window(*args, **kwargs)
        window._backend = __backend__
        config = configuration.gl_get_configuration()
        log.info("Using %s (%s %d.%d)" %
                 (__backend__.name(), config.api,
                  config.major_version, config.minor_version))

        # Display fps options
        if options.display_fps:
            @window.timer(1.0)
            def timer(elapsed):
                print "Estimated FPS:", fps()

        return window



# ----------------------------------------------------------------- __run__ ---
def __run__(clock=None, framerate=None, backend=None):
    """ Run the main loop

    Parameters
    ----------
    clock : Clock
        clock to use to run the app (gives the elementary tick)

    framerate : int
        frames per second

    backend : python module
        Backend module
    """
    global __clock__

    options = parser.get_options()

    if options.debug:
        log.setLevel(logging.DEBUG)

    if framerate is None:
        framerate = options.framerate
    if framerate > 0:
        log.info("Running at %d frames/second" % framerate)
    else:
        log.info("Running at full speed")


    if clock is None:
        __clock__ = _clock.get_default()
    else:
        __clock__ = clock
    __clock__.set_fps_limit(framerate)


    # OpenGL Initialization
    gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 1)
    gl.glPixelStorei(gl.GL_PACK_ALIGNMENT, 1)
    gl.glEnable(gl.GL_VERTEX_PROGRAM_POINT_SIZE)
    gl.glEnable(gl.GL_POINT_SPRITE)


    # Initialize timers for all windows
    for window in backend.windows():
        window._clock = __clock__

        # Start timers
        for i in range(len(window._timer_stack)):
            handler, interval = window._timer_stack[i]
            __clock__.schedule_interval(handler, interval)

        # Dispatch init event
        window.dispatch_event('on_init')

        # Dispatch an initial resize event
        window.dispatch_event('on_resize', window._width, window._height)

    # Run until no more window
    count = len(backend.windows())
    while count:
        count = backend.process(__clock__.tick())



# --------------------------------------------------------------------- run ---
def run(clock=None, framerate=None):
    """ Run the main loop

    Parameters
    ----------
    clock : Clock
        clock to use to run the app (gives the elementary tick)

    framerate : int
        frames per second
    """

    __run__(clock, framerate, __backend__)
