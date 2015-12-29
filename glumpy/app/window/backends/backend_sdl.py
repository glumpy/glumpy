# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
"""
`Pygame <http://www.pygame.org/>`_ is a set of Python modules designed for
writing games. Pygame adds functionality on top of the excellent SDL
library. This allows you to create fully featured games and multimedia programs
in the python language.

**Usage**

  .. code:: python

     from glumpy import app

     app.use("sdl")
     window = app.Window()


**Capability**

========================== ======== ======================== ========
Multiple windows              ✘     Set GL API                  ✘
-------------------------- -------- ------------------------ --------
Non-decorated windows         ✓     Set GL Profile              ✘
-------------------------- -------- ------------------------ --------
Resize windows                ✘     Share GL Context            ✘
-------------------------- -------- ------------------------ --------
Move windows                  ✘     Unicode handling            ✓
-------------------------- -------- ------------------------ --------
Fullscreen                    ✓     Scroll event                ✘
========================== ======== ======================== ========
"""
import os, sys
from glumpy import gl
from glumpy.log import log
from glumpy.app import configuration
from glumpy.app.window import window


# Backend name
__name__ = "SDL"

# Backend version (if available)
__version__ = ""

# Backend availability
__availability__ = False

# Whether the framework has been initialized
__initialized__ = False

# Active windows
__windows__ = []

# Configuration flags
__flags__ = None


# ---------------------------------------------------- convenient functions ---
def name():      return __name__
def version():   return __version__
def available(): return __availability__


# --------------------------------------------------------------- init/exit ---
def __init__():
    global __initialized__
    if not __initialized__:
        os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
        pygame.init()

    __initialized__ = True

def __exit__():
    global __initialized__
    pygame.quit()
    __initialized__ = False


# ------------------------------------------------------------ availability ---
try:
    import pygame
    if not __initialized__:
        __init__()
    __availability__ = True
    __version__ = ("%d.%d.%d") % pygame.version.vernum

    __mouse_map__ = { 0:                  window.mouse.LEFT,
                      1:                  window.mouse.MIDDLE,
                      2:                  window.mouse.RIGHT }

    __key_map__   = { 0x008:              window.key.BACKSPACE,
                      0x009:              window.key.TAB,
                      0x00A:              window.key.LINEFEED,
                      0x00C:              window.key.CLEAR,
                      0x00D:              window.key.RETURN,
                      0x018:              window.key.CANCEL,
                      0x01B:              window.key.ESCAPE,
                      pygame.K_F1:        window.key.F1,
                      pygame.K_F2:        window.key.F2,
                      pygame.K_F3:        window.key.F3,
                      pygame.K_F4:        window.key.F4,
                      pygame.K_F5:        window.key.F5,
                      pygame.K_F6:        window.key.F6,
                      pygame.K_F7:        window.key.F7,
                      pygame.K_F8:        window.key.F8,
                      pygame.K_F9:        window.key.F9,
                      pygame.K_F10:       window.key.F10,
                      pygame.K_F11:       window.key.F11,
                      pygame.K_F12:       window.key.F12,
                      pygame.K_LEFT:      window.key.LEFT,
                      pygame.K_UP:        window.key.UP,
                      pygame.K_RIGHT:     window.key.RIGHT,
                      pygame.K_DOWN:      window.key.DOWN,
                      pygame.K_PAGEUP:    window.key.PAGEUP,
                      pygame.K_PAGEDOWN:  window.key.PAGEDOWN,
                      pygame.K_HOME:      window.key.HOME,
                      pygame.K_END:       window.key.END,
                      pygame.K_INSERT:    window.key.INSERT }


except ImportError:
    __availability__ = False
    __version__ = None


# -------------------------------------------------------------- capability ---
capability = {
    "Window position get/set" : False,
    "Window size get/set"     : False,
    "Multiple windows"        : False,
    "Mouse scroll events"     : False,
    "Non-decorated window"    : True,
    "Non-sizeable window"     : True,
    "Fullscreen mode"         : True,
    "Unicode processing"      : False,
    "Set GL version"          : False,
    "Set GL profile"          : False,
    "Share GL context"        : False,
}


# ------------------------------------------------------- set_configuration ---
def set_configuration(configuration):
    """ Set gl configuration """

    global __flags__
    pygame.display.gl_set_attribute( pygame.GL_SWAP_CONTROL, 0 )
    pygame.display.gl_set_attribute( pygame.GL_RED_SIZE, configuration.red_size)
    pygame.display.gl_set_attribute( pygame.GL_GREEN_SIZE, configuration.green_size)
    pygame.display.gl_set_attribute( pygame.GL_BLUE_SIZE, configuration.blue_size)
    pygame.display.gl_set_attribute( pygame.GL_ALPHA_SIZE, configuration.alpha_size)
    pygame.display.gl_set_attribute( pygame.GL_DEPTH_SIZE, configuration.depth_size)
    pygame.display.gl_set_attribute( pygame.GL_STENCIL_SIZE, configuration.stencil_size)
    if configuration.samples:
        pygame.display.gl_set_attribute( pygame.GL_MULTISAMPLEBUFFERS, 1)
        pygame.display.gl_set_attribute( pygame.GL_MULTISAMPLESAMPLES, configuration.samples)
    else:
        pygame.display.gl_set_attribute( pygame.GL_MULTISAMPLEBUFFERS, 0)
        pygame.display.gl_set_attribute( pygame.GL_MULTISAMPLESAMPLES, 0)
    pygame.display.gl_set_attribute( pygame.GL_STEREO, configuration.stereo)
    if configuration.double_buffer:
        __flags__ = pygame.HWSURFACE | pygame.OPENGL | pygame.DOUBLEBUF
    else:
        __flags__ = pygame.HWSURFACE | pygame.OPENGL



# ------------------------------------------------------------------ Window ---
class Window(window.Window):
    ''' '''

    def __init__( self, width=256, height=256, title=None, visible=True, aspect=None,
                  decoration=True, fullscreen=False, config=None, context=None, color=(0,0,0,1)):

        if len(__windows__) > 0:
            log.critical(
                """SDL backend cannot have more than one window.\n"""
                """Exiting...""")
            sys.exit(0)

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

        flags = __flags__
        if self._decoration == False:
            flags = __flags__ | pygame.NOFRAME

        pygame.display.set_mode((width, height), flags)
        pygame.display.set_caption(self._title)
        __windows__.append(self)


    def process_event(self, event):

        if event.type == pygame.VIDEORESIZE:
            width, height = event.w, event.h
            self.dispatch_event("on_resize", width, height)

        elif event.type == pygame.QUIT:
            self.close()

        elif event.type == pygame.MOUSEMOTION:
            x,y = pygame.mouse.get_pos()
            buttons = pygame.mouse.get_pressed()
            dx = x - self._mouse_x
            dy = y - self._mouse_y
            self._mouse_x = x
            self._mouse_y = y
            if buttons[0]:
                self.dispatch_event("on_mouse_drag", x, y, dx, dy, window.mouse.LEFT)
            elif buttons[1]:
                self.dispatch_event("on_mouse_drag", x, y, dx, dy, window.mouse.MIDDLE)
            elif buttons[2]:
                self.dispatch_event("on_mouse_drag", x, y, dx, dy, window.mouse.RIGHT)
            else:
                self.dispatch_event("on_mouse_motion", x, y, dx, dy)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x,y = pygame.mouse.get_pos()
            self._mouse_x = x
            self._mouse_y = y
            button = __mouse_map__.get(event.button, window.mouse.UNKNOWN)
            self.dispatch_event("on_mouse_press", x, y, button)

        elif event.type == pygame.MOUSEBUTTONUP:
            x,y = pygame.mouse.get_pos()
            self._mouse_x = x
            self._mouse_y = y
            button = __mouse_map__.get(event.button, window.mouse.UNKNOWN)
            self.dispatch_event("on_mouse_release", x, y, button)

        elif event.type == pygame.KEYUP:
            modifiers = self._modifiers_translate(event.mod)
            symbol = self._keyboard_translate(event.key)
            self.dispatch_event("on_key_press", symbol, modifiers)

        elif event.type == pygame.KEYDOWN:
            modifiers = self._modifiers_translate(event.mod)
            symbol = self._keyboard_translate(event.key)
            self.dispatch_event("on_key_release", symbol, modifiers)


    def _modifiers_translate( self, modifiers ):
        _modifiers = 0
        if modifiers & (pygame.K_LSHIFT | pygame.K_RSHIFT):
            _modifiers |=  window.key.MOD_SHIFT
        if modifiers & (pygame.K_LCTRL | pygame.K_RCTRL):
            _modifiers |=  window.key.MOD_CTRL
        if modifiers & (pygame.K_LALT | pygame.K_RALT):
            _modifiers |=  window.key.MOD_ALT
        return _modifiers

    def _keyboard_translate(self, code):
        ascii = code
        if (0x020 <= ascii <= 0x040) or (0x05b <= ascii <= 0x07e):
            return ascii
        elif ascii <= 0x020:
            code = ascii
        return __key_map__.get(code, window.key.UNKNOWN)

    def close(self):
        __windows__.remove(self)
        self.dispatch_event("on_close")

    def swap(self):
        pygame.display.flip()

    def activate(self):
        pass


# ----------------------------------------------------------------- windows ---
def windows():
    return __windows__


# ----------------------------------------------------------------- process ---
def process(dt):

    if not len(__windows__):
        return 0

    window = __windows__[0]

    # Poll for and process events
    for event in pygame.event.get():
        window.process_event(event)

    # Activate window
    window.activate()

    # Dispatch the main draw event
    window.dispatch_event('on_draw', dt)

    # Dispatch the idle event
    window.dispatch_event('on_idle', dt)

    # Swap buffers
    window.swap()

    return 1
