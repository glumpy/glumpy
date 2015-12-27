# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
"""
`Pyglet <www.pyglet.org>`_ is a pure python cross-platform application
framework intended for game development. It supports windowing, user interface
event handling, OpenGL graphics, loading images and videos and playing sounds
and music. It works on Windows, OS X and Linux.

**Usage**

  .. code:: python

     from glumpy import app

     app.use("pyglet")
     window = app.Window()


**Capability**

========================== ======== ======================== ========
Multiple windows              ✓     Set GL API                  ✘    
-------------------------- -------- ------------------------ --------
Non-decorated windows         ✓     Set GL Profile              ✘    
-------------------------- -------- ------------------------ --------
Resize windows                ✓     Share GL Context            ✓    
-------------------------- -------- ------------------------ --------
Move windows                  ✓     Unicode handling            ✓    
-------------------------- -------- ------------------------ --------
Fullscreen                    ✓     Scroll event                ✓    
========================== ======== ======================== ========
"""
import sys
from glumpy import gl
from glumpy.log import log
from glumpy.app import configuration
from glumpy.app.window import window


# Backend name
__name__ = "Pyglet"

# Backend version (if available)
__version__ = ""

# Whether the framework has been initialized
__initialized__ = False

# Backend availability
__availability__ = False

# Active windows
__windows__ = []

# Default configuration
__configuration__ = None


# ---------------------------------------------------- convenient functions ---
def name():      return __name__
def version():   return __version__
def available(): return __availability__


# --------------------------------------------------------------- init/exit ---
def __init__():
    global __initialized__
    __initialized__ = True

def __exit__():
    global __initialized__
    # Not an error, we cannot really terminate pyglet
    __initialized__ = True


# ------------------------------------------------------------ availability ---
try:
    import pyglet
    __availability__ = True
    __version__ = pyglet.version
    __init__()
except ImportError:
    __availability__ = False
    __version__ = None


# -------------------------------------------------------------- capability ---
capability = {
    "Window position get/set" : True,
    "Window size get/set"     : True,
    "Multiple windows"        : True,
    "Mouse scroll events"     : True,
    "Non-decorated window"    : True,
    "Non-sizeable window"     : True,
    "Fullscreen mode"         : True,
    "Unicode processing"      : True,
    "Set GL version"          : False,
    "Set GL profile"          : False,
    "Share GL context"        : True,
}




# ------------------------------------------------------- set_configuration ---
def set_configuration(config):
    """ Set gl configuration """

    global __configuration__

    __configuration__ = pyglet.gl.Config()

    __configuration__.red_size = config.red_size
    __configuration__.green_size = config.green_size
    __configuration__.blue_size = config.blue_size
    __configuration__.alpha_size = config.alpha_size

    __configuration__.accum_red_size = 0
    __configuration__.accum_green_size = 0
    __configuration__.accum_blue_size = 0
    __configuration__.accum_alpha_size = 0

    __configuration__.depth_size = config.depth_size
    __configuration__.stencil_size = config.stencil_size
    __configuration__.double_buffer = config.double_buffer
    __configuration__.stereo = config.stereo
    __configuration__.samples = config.samples




# ------------------------------------------------------------------ Window ---
class Window(window.Window):


    def __init__( self, width=256, height=256, title=None, visible=True, aspect=None,
                  decoration=True, fullscreen=False, config=None, context=None, color=(0,0,0,1)):

        window.Window.__init__(self, width=width,
                                     height=height,
                                     title=title,
                                     visible=visible,
                                     aspect=aspect,
                                     decoration=decoration,
                                     fullscreen=fullscreen,
                                     config=config,
                                     context=context,
                                     color=color)

        if config is None:
            config = configuration.Configuration()
        set_configuration(config)

        self._native_window = pyglet.window.Window(
            width=self._width, height=self._height, caption=title,
            resizable=True, vsync=False, config=__configuration__)

        def on_mouse_drag(x, y, dx, dy, button, modifiers):
            # BUGFIX
            self.dispatch_event("on_mouse_drag", x, y, dx, -dy, button)
        self._native_window.on_mouse_drag = on_mouse_drag

        def on_mouse_enter(x, y):
            y = self.height-y
            self.dispatch_event("on_enter", x, y)
        self._native_window.on_mouse_enter = on_mouse_enter

        def on_mouse_leave(x, y):
            y = self.height-y
            self.dispatch_event("on_leave", x, y)
        self._native_window.on_mouse_leave = on_mouse_leave

        def on_mouse_motion(x, y, dx, dy):
            self.dispatch_event("on_mouse_motion", x, y, dx, -dy)
        self._native_window.on_mouse_motion = on_mouse_motion

        def on_mouse_press(x, y, button, modifiers):
            self.dispatch_event("on_mouse_press", x, y, button)
        self._native_window.on_mouse_press = on_mouse_press

        def on_mouse_release(x, y, button, modifiers):
            self.dispatch_event("on_mouse_release", x, y, button)
        self._native_window.on_mouse_release = on_mouse_release

        def on_mouse_scroll(x, y, scroll_x, scroll_y):
            # BUGFIX
            y = self.height-y
            self.dispatch_event("on_mouse_scroll", x, y, scroll_x, -scroll_y)
        self._native_window.on_mouse_scroll = on_mouse_scroll

        def on_resize(width, height):
            self.dispatch_event("on_resize", width, height)
        self._native_window.on_resize = on_resize

        def on_show():
            self.dispatch_event("on_show")
        self._native_window.on_show = on_show

        def on_hide():
            self.dispatch_event("on_hide")
        self._native_window.on_hide = on_hide

        def on_close():
            self.close()
        self._native_window.on_close = on_close

        def on_key_press(symbol, modifiers):
            self.dispatch_event("on_key_press", symbol, modifiers)
        self._native_window.on_key_press = on_key_press

        def on_key_release(symbol, modifiers):
            self.dispatch_event("on_key_release", symbol, modifiers)
        self._native_window.on_key_release = on_key_release

        def on_draw():
            self.dispatch_event("on_draw")
        self._native_window.on_draw = on_draw

        __windows__.append(self)


    def close(self):
        self._native_window.close()
        __windows__.remove(self)
        for i in range(len(self._timer_stack)):
            handler, interval = self._timer_stack[i]
            self._clock.unschedule(handler)
        self.dispatch_event("on_close")

    def show(self):
        self._native_window.set_visible(True)

    def hide(self):
        self._native_window.set_visible(False)

    def set_fullscreen(self, state):
        self._native_window.set_fullscreen(state)

    def set_title(self, title):
        self._native_window.set_caption(title)
        self._title = title

    def get_title(self, title):
        return self._title

    def set_size(self, width, height):
        self._window.set_size(width, height)
        self._width  = self._native_window.width
        self._height = self._native_window.height

    def get_size(self):
        self._width  = self._native_window.width
        self._height = self._native_window.height
        return self._width, self._height

    def set_position(self, x, y):
        self._native_window.set_location(x,y)
        self._x, self._y = self._native_window.get_location()

    def get_position(self):
        self._x, self._y = self._native_window.get_location()
        return self._x, self._y

    def swap(self):
        self._native_window.flip()

    def activate(self):
        self._native_window.switch_to()


# ----------------------------------------------------------------- windows ---
def windows():
    return __windows__


# ----------------------------------------------------------------- process ---
def process(dt):

    for window in __windows__:

        # Activate window
        window.activate()

        # Dispatch any pending event
        window._native_window.dispatch_events()

        # Dispatch the main draw event
        window.dispatch_event('on_draw', dt)

        # Dispatch the idle event
        window.dispatch_event('on_idle', dt)

        # Swap buffers
        window.swap()

    return len(__windows__)
