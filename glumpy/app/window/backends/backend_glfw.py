# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
"""
`GLFW <http://www.glfw.org>`_ is an Open Source, multi-platform library for
creating windows with OpenGL contexts and receiving input and events. It is
easy to integrate into existing applications and does not lay claim to the main
loop.

**Usage**

  .. code:: python

     from glumpy import app

     app.use("glfw")
     window = app.Window()


**Capability**

========================== ======== ======================== ========
Multiple windows              ✓     Set GL API                  ✓    
-------------------------- -------- ------------------------ --------
Non-decorated windows         ✓     Set GL Profile              ✓    
-------------------------- -------- ------------------------ --------
Resize windows                ✓     Share GL Context            ✓    
-------------------------- -------- ------------------------ --------
Move windows                  ✓     Unicode handling            ✓    
-------------------------- -------- ------------------------ --------
Fullscreen                    ✓     Scroll event                ✓    
========================== ======== ======================== ========
"""
import os, sys
from glumpy import gl
from glumpy.log import log
from glumpy.app import configuration
from glumpy.app.window import window


# Backend name
__name__ = "GLFW"

# Backend version (if available)
__version__ = ""

# Backend availability
__availability__ = False

# Whether the framework has been initialized
__initialized__ = False

# Active windows
__windows__ = []


# ---------------------------------------------------- convenient functions ---
def name():      return __name__
def version():   return __version__
def available(): return __availability__


# --------------------------------------------------------------- init/exit ---
def __init__():
    global __initialized__
    if not __initialized__:
        # glfw might change dir on initialization (feature, not a bug)
        cwd = os.getcwd()
        glfw.glfwInit()
        os.chdir(cwd)
    __initialized__ = True

def __exit__():
    global __initialized__
    glfw.glfwTerminate()
    __initialized__ = False


# ------------------------------------------------------------ availability ---
try:
    from glumpy.ext import glfw
    __availability__ = True
    __version__ = ("%d.%d.%d") % glfw.version
    __init__()

    __mouse_map__ = { glfw.GLFW_MOUSE_BUTTON_LEFT:   window.mouse.LEFT,
                      glfw.GLFW_MOUSE_BUTTON_MIDDLE: window.mouse.MIDDLE,
                      glfw.GLFW_MOUSE_BUTTON_RIGHT:  window.mouse.RIGHT }

    __key_map__   = { glfw.GLFW_KEY_ESCAPE:        window.key.ESCAPE,
                      glfw.GLFW_KEY_ENTER:         window.key.ENTER,
                      glfw.GLFW_KEY_TAB:           window.key.TAB,
                      glfw.GLFW_KEY_BACKSPACE:     window.key.BACKSPACE,
                      glfw.GLFW_KEY_INSERT:        window.key.INSERT,
                      glfw.GLFW_KEY_DELETE:        window.key.DELETE,
                      glfw.GLFW_KEY_RIGHT:         window.key.RIGHT,
                      glfw.GLFW_KEY_LEFT:          window.key.LEFT,
                      glfw.GLFW_KEY_DOWN:          window.key.DOWN,
                      glfw.GLFW_KEY_UP:            window.key.UP,
                      glfw.GLFW_KEY_PAGE_UP:       window.key.PAGEUP,
                      glfw.GLFW_KEY_PAGE_DOWN:     window.key.PAGEDOWN,
                      glfw.GLFW_KEY_HOME:          window.key.HOME,
                      glfw.GLFW_KEY_END:           window.key.END,
                      glfw.GLFW_KEY_CAPS_LOCK:     window.key.CAPSLOCK,
                      glfw.GLFW_KEY_PRINT_SCREEN:  window.key.PRINT,
                      glfw.GLFW_KEY_PAUSE:         window.key.PAUSE,
                      glfw.GLFW_KEY_F1:            window.key.F1,
                      glfw.GLFW_KEY_F2:            window.key.F2,
                      glfw.GLFW_KEY_F3:            window.key.F3,
                      glfw.GLFW_KEY_F4:            window.key.F4,
                      glfw.GLFW_KEY_F5:            window.key.F5,
                      glfw.GLFW_KEY_F6:            window.key.F6,
                      glfw.GLFW_KEY_F7:            window.key.F7,
                      glfw.GLFW_KEY_F8:            window.key.F8,
                      glfw.GLFW_KEY_F9:            window.key.F9,
                      glfw.GLFW_KEY_F10:           window.key.F10,
                      glfw.GLFW_KEY_F11:           window.key.F11,
                      glfw.GLFW_KEY_F12:           window.key.F12 }

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
    "Set GL version"          : True,
    "Set GL profile"          : True,
    "Share GL context"        : True,
}


# ------------------------------------------------------- set_configuration ---
def set_configuration(config):
    """ Set gl configuration for GLFW """

    glfw.glfwWindowHint( glfw.GLFW_REFRESH_RATE, 0 )

    glfw.glfwWindowHint(glfw.GLFW_RED_BITS, config.red_size)
    glfw.glfwWindowHint(glfw.GLFW_GREEN_BITS, config.green_size)
    glfw.glfwWindowHint(glfw.GLFW_BLUE_BITS, config.blue_size)
    glfw.glfwWindowHint(glfw.GLFW_ALPHA_BITS, config.alpha_size)

    glfw.glfwWindowHint(glfw.GLFW_ACCUM_RED_BITS, 0)
    glfw.glfwWindowHint(glfw.GLFW_ACCUM_GREEN_BITS, 0)
    glfw.glfwWindowHint(glfw.GLFW_ACCUM_BLUE_BITS, 0)
    glfw.glfwWindowHint(glfw.GLFW_ACCUM_ALPHA_BITS, 0)

    glfw.glfwWindowHint(glfw.GLFW_DEPTH_BITS, config.depth_size)
    glfw.glfwWindowHint(glfw.GLFW_STENCIL_BITS, config.stencil_size)
    glfw.glfwWindowHint(glfw.GLFW_SRGB_CAPABLE, config.srgb)
    glfw.glfwWindowHint(glfw.GLFW_SAMPLES, config.samples)
    glfw.glfwWindowHint(glfw.GLFW_STEREO, config.stereo)

    if config.api in ("ES", "es"):
        glfw.glfwWindowHint(glfw.GLFW_CLIENT_API,
                            glfw.GLFW_OPENGL_ES_API)
    else:
        glfw.glfwWindowHint(glfw.GLFW_CONTEXT_VERSION_MAJOR,
                            config.major_version)
        glfw.glfwWindowHint(glfw.GLFW_CONTEXT_VERSION_MINOR,
                            config.minor_version)

        if config.major_version >= 3 and config.profile == "core":
            glfw.glfwWindowHint(glfw.GLFW_OPENGL_PROFILE,
                                glfw.GLFW_OPENGL_CORE_PROFILE)
            glfw.glfwWindowHint(glfw.GLFW_OPENGL_FORWARD_COMPAT, True)
        elif config.major_version >= 3 and config.profile == "compatibility":
            glfw.glfwWindowHint(glfw.GLFW_OPENGL_PROFILE,
                                glfw.GLFW_OPENGL_COMPAT_PROFILE)
        else:
            glfw.glfwWindowHint(glfw.GLFW_OPENGL_PROFILE,
                                glfw.GLFW_OPENGL_ANY_PROFILE)


# ------------------------------------------------------------------ Window ---
class Window(window.Window):

    def __init__( self, width=512, height=512, title=None, visible=True, aspect=None,
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

        # Whether hidpi is active
        self._hidpi = False

        def on_error(error, message):
            log.warning(message)
        glfw.glfwSetErrorCallback(on_error)

        glfw.glfwWindowHint(glfw.GLFW_RESIZABLE, True)
        glfw.glfwWindowHint(glfw.GLFW_DECORATED, True)
        glfw.glfwWindowHint(glfw.GLFW_VISIBLE, True)
        if not decoration:
            glfw.glfwWindowHint(glfw.GLFW_DECORATED, False)
        if not visible:
            glfw.glfwWindowHint(glfw.GLFW_VISIBLE, False)

        if config is None:
            config = configuration.Configuration()
        set_configuration(config)
        self._native_window = glfw.glfwCreateWindow( self._width, self._height,
                                                     self._title, None, None)

        if not self._native_window:
            log.critical("Window creation failed")
            __exit__()
            sys.exit()

        glfw.glfwMakeContextCurrent(self._native_window)
        glfw.glfwSwapInterval(0)

        # OSX: check framebuffer size / window size. On retina display, they
        #      can be different so we try to correct window size such as having
        #      the framebuffer size of the right size
        w,h = glfw.glfwGetFramebufferSize(self._native_window)
        if w != width or h!= height:
            width, height  = width//2, height//2
            glfw.glfwSetWindowSize(self._native_window, width, height)
            log.info("HiDPI detected, fixing window size")
            self._hidpi = True


        def on_framebuffer_resize(win, width, height):
            self._width, self._height = width, height
            self.dispatch_event('on_resize', width, height)
        glfw.glfwSetFramebufferSizeCallback(self._native_window, on_framebuffer_resize)
        # def on_resize(win, width, height):
        #     self._width, self._height = width, height
        #     self.dispatch_event('on_resize', width, height)
        # glfw.glfwSetWindowSizeCallback(self._native_window, on_resize)


        def on_cursor_enter(win, entered):
            if entered:
                self.dispatch_event('on_enter')
            else:
                self.dispatch_event('on_leave')
        glfw.glfwSetCursorEnterCallback(self._native_window, on_cursor_enter)


        def on_window_close(win):
            self.close()
        glfw.glfwSetWindowCloseCallback(self._native_window, on_window_close)


        def on_keyboard(win, key, scancode, action, mods):
            symbol = self._keyboard_translate(key)
            modifiers = self._modifiers_translate(mods)
            if action in[glfw.GLFW_PRESS,glfw.GLFW_REPEAT]:
                self.dispatch_event('on_key_press', symbol, modifiers)
            else:
                self.dispatch_event('on_key_release', symbol, modifiers)
        glfw.glfwSetKeyCallback(self._native_window, on_keyboard)


        def on_character(win, character):
            self.dispatch_event('on_character', u"%c" % character)
        glfw.glfwSetCharCallback(self._native_window, on_character)


        def on_mouse_button(win, button, action, mods):
            x,y = glfw.glfwGetCursorPos(win)
            if self._hidpi:
                x, y = 2*x, 2*y

            button = __mouse_map__.get(button, window.mouse.UNKNOWN)
            if action == glfw.GLFW_RELEASE:
                self._button = window.mouse.NONE
                self._mouse_x = x
                self._mouse_y = y
                self.dispatch_event('on_mouse_release', x, y, button)
            elif action == glfw.GLFW_PRESS:
                self._button = button
                self._mouse_x = x
                self._mouse_y = y
                self.dispatch_event('on_mouse_press', x, y, button)
        glfw.glfwSetMouseButtonCallback(self._native_window, on_mouse_button)


        def on_mouse_motion(win, x, y):
            if self._hidpi:
                x, y = 2*x, 2*y
            dx = x - self._mouse_x
            dy = y - self._mouse_y
            self._mouse_x = x
            self._mouse_y = y
            if self._button != window.mouse.NONE:
                self.dispatch_event('on_mouse_drag', x, y, dx, dy, self._button)
            else:
                self.dispatch_event('on_mouse_motion', x, y, dx, dy)
        glfw.glfwSetCursorPosCallback(self._native_window, on_mouse_motion)


        def on_scroll(win, xoffset, yoffset):
            x,y = glfw.glfwGetCursorPos(win)
            if self._hidpi:
                x, y = 2*x, 2*y
            self.dispatch_event('on_mouse_scroll', x, y, xoffset, yoffset)
        glfw.glfwSetScrollCallback( self._native_window, on_scroll )

        self._width, self._height = self.get_size()
        __windows__.append(self)


    def _modifiers_translate( self, modifiers ):
        _modifiers = 0
        if modifiers & glfw.GLFW_MOD_SHIFT:
            _modifiers |=  window.key.MOD_SHIFT
        if modifiers & glfw.GLFW_MOD_CONTROL:
            _modifiers |=  window.key.MOD_CTRL
        if modifiers & glfw.GLFW_MOD_ALT:
            _modifiers |=  window.key.MOD_ALT
        if modifiers & glfw.GLFW_MOD_SUPER:
            _modifiers |=  window.key.MOD_COMMAND
        self._modifiers = modifiers
        return _modifiers

    def _keyboard_translate( self, code ):
        if (32 <= code <= 96) or code in [161,162]:
            return code
        return __key_map__.get(code, window.key.UNKNOWN)


    def show(self):
        glfw.glfwShowWindow( self._native_window )
        self.dispatch_event('on_show')

    def hide(self):
        glfw.glfwHideWindow( self._native_window )
        self.dispatch_event('on_hide')

    def close(self):
        glfw.glfwSetWindowShouldClose(self._native_window, True)
        glfw.glfwDestroyWindow(self._native_window)
        __windows__.remove(self)
        for i in range(len(self._timer_stack)):
            handler, interval = self._timer_stack[i]
            self._clock.unschedule(handler)
        self.dispatch_event('on_close')

    def set_title(self, title):
        glfw.glfwSetWindowTitle( self._native_window, title)
        self._title = title

    def get_title(self, title):
        return self._title

    def set_size(self, width, height):
        glfw.glfwSetWindowSize(self._native_window, width, height)
        self._width, self._height = glfw.glfwGetFramebufferSize(self._native_window)

    def get_size(self):
        # self._width, self._height = glfw.glfwGetWindowSize(self._native_window)
        self._width, self._height = glfw.glfwGetFramebufferSize(self._native_window)
        return self._width, self._height

    def set_position(self, x, y):
        glfw.glfwSetWindowPos(self._native_window, x, y)
        self._x, self._y = glfw.glfwGetWindowPos(self._native_window)

    def get_position(self):
        self._x, self._y = glfw.glfwGetWindowPos(self._native_window)
        return self._x, self._y

    def swap(self):
        glfw.glfwSwapBuffers(self._native_window)

    def activate(self):
        glfw.glfwMakeContextCurrent(self._native_window)



# ----------------------------------------------------------------- windows ---
def windows():
    return __windows__


# ----------------------------------------------------------------- process ---
def process(dt):

    # Poll for and process events
    glfw.glfwPollEvents()

    for window in __windows__:
        # Make window active
        window.activate()

        # Dispatch the main draw event
        window.dispatch_event('on_draw', dt)

        # Dispatch the idle event
        window.dispatch_event('on_idle', dt)

        # Swap buffers
        window.swap()


    return len(__windows__)
