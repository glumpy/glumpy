# -----------------------------------------------------------------------------
# Copyright (c) 2018 Martin Lizée. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
"""
`pyimgui <https://github.com/swistakm/pyimgui>`_ is a Cython-based binding for 
the amazing dear imgui C++ library - a Bloat-free Immediate Mode Graphical 
User Interface.



**Usage**

  .. code:: python

     from glumpy import app

     app.use("pyimgui")
     window = app.Window()


**Capability**

========================== ======== ======================== ========
Multiple windows                    Set GL API                  ✓
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
# from glumpy import gl
from glumpy.log import log
from glumpy.app import configuration
from glumpy.app.window import window

# Backend name
__name__ = "pyimgui"

# Backend version (if available)
__version__ = "0.1"

# Backend availability
__availability__ = False

# Whether the framework has been initialized
__initialized__ = False

# Active windows
__windows__ = []

# Windows scheduled to be destroyed
__windows_to_remove__ = []

# ---------------------------------------------------- convenient functions ---
def name():      return __name__
def version():   return __version__
def available(): return __availability__


# --------------------------------------------------------------- init/exit ---
def __init__():
    global __initialized__
    if not __initialized__:
        cwd = os.getcwd()
        glfw.init()
        os.chdir(cwd)
    __initialized__ = True

def __exit__():
    global __initialized__
    glfw.terminate()
    __initialized__ = False


# ------------------------------------------------------------ availability ---
try:
    # We use the window and backend from pyimgui
    import glfw
    import OpenGL.GL as gl
    import imgui
    from imgui.integrations.glfw import GlfwRenderer
    __availability__ = True
    __version__ = "0.1.0"
    __init__()

    __mouse_map__ = { glfw.MOUSE_BUTTON_LEFT:   window.mouse.LEFT,
                      glfw.MOUSE_BUTTON_MIDDLE: window.mouse.MIDDLE,
                      glfw.MOUSE_BUTTON_RIGHT:  window.mouse.RIGHT }

    __key_map__   = { glfw.KEY_ESCAPE:        window.key.ESCAPE,
                      glfw.KEY_ENTER:         window.key.ENTER,
                      glfw.KEY_TAB:           window.key.TAB,
                      glfw.KEY_BACKSPACE:     window.key.BACKSPACE,
                      glfw.KEY_INSERT:        window.key.INSERT,
                      glfw.KEY_DELETE:        window.key.DELETE,
                      glfw.KEY_RIGHT:         window.key.RIGHT,
                      glfw.KEY_LEFT:          window.key.LEFT,
                      glfw.KEY_DOWN:          window.key.DOWN,
                      glfw.KEY_UP:            window.key.UP,
                      glfw.KEY_PAGE_UP:       window.key.PAGEUP,
                      glfw.KEY_PAGE_DOWN:     window.key.PAGEDOWN,
                      glfw.KEY_HOME:          window.key.HOME,
                      glfw.KEY_END:           window.key.END,
                      glfw.KEY_CAPS_LOCK:     window.key.CAPSLOCK,
                      glfw.KEY_PRINT_SCREEN:  window.key.PRINT,
                      glfw.KEY_PAUSE:         window.key.PAUSE,
                      glfw.KEY_F1:            window.key.F1,
                      glfw.KEY_F2:            window.key.F2,
                      glfw.KEY_F3:            window.key.F3,
                      glfw.KEY_F4:            window.key.F4,
                      glfw.KEY_F5:            window.key.F5,
                      glfw.KEY_F6:            window.key.F6,
                      glfw.KEY_F7:            window.key.F7,
                      glfw.KEY_F8:            window.key.F8,
                      glfw.KEY_F9:            window.key.F9,
                      glfw.KEY_F10:           window.key.F10,
                      glfw.KEY_F11:           window.key.F11,
                      glfw.KEY_F12:           window.key.F12 }

except ImportError:
    __availability__ = False
    __version__ = None


# -------------------------------------------------------------- capability ---
capability = {
    "Window position get/set" : True,
    "Window size get/set"     : True,
    "Multiple windows"        : False,
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
def set_configuration(configuration):
    """ Set GL initialization here (depth buffer size, etc.) """
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 2)
    # the OPENGL_COMPAT_PROFILE enables the mix between pyimgui and glumpy
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_COMPAT_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)



# ------------------------------------------------------------------ Window ---
class Window(window.Window):

    def __init__( self, width=512, height=512, title=None, visible=True, aspect=None,
                  decoration=True, fullscreen=False, config=None, context=None, color=(0,0,0,1), vsync=False):

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

        def on_error(error, message):
            log.warning(message)
        glfw.set_error_callback(on_error)

        glfw.window_hint(glfw.RESIZABLE, True)
        glfw.window_hint(glfw.DECORATED, True)
        glfw.window_hint(glfw.VISIBLE, True)
        if not decoration:
            glfw.window_hint(glfw.DECORATED, False)
        if not visible:
            glfw.window_hint(glfw.VISIBLE, False)

        if config is None:
            config = configuration.Configuration()
        set_configuration(config)

        self._native_window = glfw.create_window( self._width, self._height,
                                                     self._title, None, None)

        if not self._native_window:
            log.critical("Window creation failed")
            __exit__()
            sys.exit()

        glfw.make_context_current(self._native_window)
        glfw.swap_interval(1 if vsync else 0)
        self._impl = GlfwRenderer(self._native_window)

        def on_framebuffer_resize(win, width, height):
            self._width, self._height = width, height
            self.dispatch_event('on_resize', width, height)
        glfw.set_framebuffer_size_callback(self._native_window, on_framebuffer_resize)
        # def on_resize(win, width, height):
        #     self._width, self._height = width, height
        #     self.dispatch_event('on_resize', width, height)
        # glfw.set_window_size_callback(self._native_window, on_resize)

        def on_cursor_enter(win, entered):
            if entered:
                self.dispatch_event('on_enter')
            else:
                self.dispatch_event('on_leave')
        glfw.set_cursor_enter_callback(self._native_window, on_cursor_enter)


        def on_window_close(win):
            self.close()
        glfw.set_window_close_callback(self._native_window, on_window_close)


        def on_keyboard(win, key, scancode, action, mods):
            if self._impl.io.want_text_input or self._impl.io.want_capture_keyboard:
                return None
            symbol = self._keyboard_translate(key)
            modifiers = self._modifiers_translate(mods)
            if action in[glfw.PRESS,glfw.REPEAT]:
                self.dispatch_event('on_key_press', symbol, modifiers)
            else:
                self.dispatch_event('on_key_release', symbol, modifiers)
        glfw.set_key_callback(self._native_window, on_keyboard)


        def on_character(win, character):
            if self._impl.io.want_text_input or self._impl.io.want_capture_keyboard:
                return None
            self.dispatch_event('on_character', u"%c" % character)
        glfw.set_char_callback(self._native_window, on_character)


        def on_mouse_button(win, button, action, mods):
            if self._impl.io.want_capture_mouse:
                return None
            x,y = glfw.get_cursor_pos(win)

            button = __mouse_map__.get(button, window.mouse.UNKNOWN)
            if action == glfw.RELEASE:
                self._button = window.mouse.NONE
                self._mouse_x = x
                self._mouse_y = y
                self.dispatch_event('on_mouse_release', x, y, button)
            elif action == glfw.PRESS:
                self._button = button
                self._mouse_x = x
                self._mouse_y = y
                self.dispatch_event('on_mouse_press', x, y, button)
        glfw.set_mouse_button_callback(self._native_window, on_mouse_button)


        def on_mouse_motion(win, x, y):
            if self._impl.io.want_capture_mouse:
               return None
            dx = x - self._mouse_x
            dy = y - self._mouse_y
            self._mouse_x = x
            self._mouse_y = y
            if self._button != window.mouse.NONE:
                self.dispatch_event('on_mouse_drag', x, y, dx, dy, self._button)
            else:
                self.dispatch_event('on_mouse_motion', x, y, dx, dy)
        glfw.set_cursor_pos_callback(self._native_window, on_mouse_motion)


        def on_scroll(win, xoffset, yoffset):
            if self._impl.io.want_capture_mouse:
                return None
            x,y = glfw.get_cursor_pos(win)
            self.dispatch_event('on_mouse_scroll', x, y, xoffset, yoffset)
        glfw.set_scroll_callback( self._native_window, on_scroll )

        self._width, self._height = self.get_size()
        __windows__.append(self)


    def _modifiers_translate( self, modifiers ):
        _modifiers = 0
        if modifiers & glfw.MOD_SHIFT:
            _modifiers |=  window.key.MOD_SHIFT
        if modifiers & glfw.MOD_CONTROL:
            _modifiers |=  window.key.MOD_CTRL
        if modifiers & glfw.MOD_ALT:
            _modifiers |=  window.key.MOD_ALT
        if modifiers & glfw.MOD_SUPER:
            _modifiers |=  window.key.MOD_COMMAND
        self._modifiers = modifiers
        return _modifiers

    def _keyboard_translate( self, code ):
        if (32 <= code <= 96) or code in [161,162]:
            return code
        return __key_map__.get(code, window.key.UNKNOWN)


    def show(self):
        glfw.show_window( self._native_window )
        self.dispatch_event('on_show')

    def hide(self):
        glfw.hide_window( self._native_window )
        self.dispatch_event('on_hide')

    def close(self):
        glfw.set_window_should_close(self._native_window, True)
        __windows__.remove(self)
        __windows_to_remove__.append(self)
        for i in range(len(self._timer_stack)):
            handler, interval = self._timer_stack[i]
            self._clock.unschedule(handler)
        self.dispatch_event('on_close')

    def destroy(self):
        glfw.destroy_window(self._native_window)

    def set_title(self, title):
        glfw.set_window_title( self._native_window, title)
        self._title = title

    def get_title(self, title):
        return self._title

    def set_size(self, width, height):
        glfw.set_window_size(self._native_window, width, height)
        self._width, self._height = glfw.get_framebuffer_size(self._native_window)

    def get_size(self):
        # self._width, self._height = glfw.get_window_size(self._native_window)
        self._width, self._height = glfw.get_framebuffer_size(self._native_window)
        return self._width, self._height

    def set_position(self, x, y):
        glfw.set_window_pos(self._native_window, x, y)
        self._x, self._y = glfw.get_window_pos(self._native_window)

    def get_position(self):
        self._x, self._y = glfw.get_window_pos(self._native_window)
        return self._x, self._y

    def swap(self):
        glfw.swap_buffers(self._native_window)

    def activate(self):
        glfw.make_context_current(self._native_window)

    def new_frame(self):
        imgui.new_frame()

    def render_gui(self):
        imgui.render()
        self._impl.render(imgui.get_draw_data())



# ----------------------------------------------------------------- windows ---
def windows():
    return __windows__

# ----------------------------------------------------------------- process ---
def process(dt):

    # Poll for and process events
    glfw.poll_events()

    for window in __windows__:
        # Make window active
        window.activate()

        # Process imgui inputs
        window._impl.process_inputs()

        # Dispatch the main draw event
        window.dispatch_event('on_draw', dt)

        # Dispatch the idle event
        window.dispatch_event('on_idle', dt)

        # Swap buffers
        window.swap()

    for window in __windows_to_remove__:
        window.destroy()
        __windows_to_remove__.remove(window)

    return len(__windows__)
