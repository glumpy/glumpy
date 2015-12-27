# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
"""
`PySDL2 <http://pysdl2.readthedocs.org/en/latest/index.html>`_ is a wrapper
around the SDL2 library and as such similar to the discontinued PySDL
project. In contrast to PySDL, it has no licensing restrictions, nor does it
rely on C code, but uses ctypes instead.

**Usage**

  .. code:: python

     from glumpy import app

     app.use("sdl2")
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
import sys, ctypes
from glumpy import gl
from glumpy.log import log
from glumpy.app import configuration
from glumpy.app.window import window


# Backend name
__name__ = "SDL2"

# Backend version (if available)
__version__ = ""

# Backend availability
__availability__ = False

# Whether the framework has been initialized
__initialized__ = False

# Active windows
__windows__ = {}


# ---------------------------------------------------- convenient functions ---
def name():      return __name__
def version():   return __version__
def available(): return __availability__


# --------------------------------------------------------------- init/exit ---
def __init__():
    global __initialized__
    if not __initialized__:
        sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)
    __initialized__ = True

def __exit__():
    global __initialized__
    sdl2.SDL_Quit()
    __initialized__ = False


# ------------------------------------------------------------ availability ---
try:
    import sdl2
    if not __initialized__:
        __init__()
    __availability__ = True
    __version__ = ("%d.%d.%d") % sdl2.version_info[:3]


    __mouse_map__ = {sdl2.SDL_BUTTON_LEFT: window.mouse.LEFT,
                     sdl2.SDL_BUTTON_MIDDLE: window.mouse.MIDDLE,
                     sdl2.SDL_BUTTON_RIGHT: window.mouse.RIGHT }
    __key_map__ = {
        # sdl2.SDLK_LSHIFT:    window.key.SHIFT,
        # sdl2.SDLK_RSHIFT:    window.key.SHIFT,
        # sdl2.SDLK_LCTRL:     window.key.CONTROL,
        # sdl2.SDLK_RCTRL:     window.key.CONTROL,
        # sdl2.SDLK_LALT:      window.key.ALT,
        # sdl2.SDLK_RALT:      window.key.ALT,
        # sdl2.SDLK_LGUI:      window.key.META,
        # sdl2.SDLK_RGUI:      window.key.META,

        sdl2.SDLK_LEFT:      window.key.LEFT,
        sdl2.SDLK_UP:        window.key.UP,
        sdl2.SDLK_RIGHT:     window.key.RIGHT,
        sdl2.SDLK_DOWN:      window.key.DOWN,
        sdl2.SDLK_PAGEUP:    window.key.PAGEUP,
        sdl2.SDLK_PAGEDOWN:  window.key.PAGEDOWN,

        sdl2.SDLK_INSERT:    window.key.INSERT,
        sdl2.SDLK_DELETE:    window.key.DELETE,
        sdl2.SDLK_HOME:      window.key.HOME,
        sdl2.SDLK_END:       window.key.END,

        sdl2.SDLK_ESCAPE:    window.key.ESCAPE,
        sdl2.SDLK_BACKSPACE: window.key.BACKSPACE,

        sdl2.SDLK_F1:         window.key.F1,
        sdl2.SDLK_F2:         window.key.F2,
        sdl2.SDLK_F3:         window.key.F3,
        sdl2.SDLK_F4:         window.key.F4,
        sdl2.SDLK_F5:         window.key.F5,
        sdl2.SDLK_F6:         window.key.F6,
        sdl2.SDLK_F7:         window.key.F7,
        sdl2.SDLK_F8:         window.key.F8,
        sdl2.SDLK_F9:         window.key.F9,
        sdl2.SDLK_F10:        window.key.F10,
        sdl2.SDLK_F11:        window.key.F11,
        sdl2.SDLK_F12:        window.key.F12,

        sdl2.SDLK_SPACE:      window.key.SPACE,
        sdl2.SDLK_RETURN:     window.key.ENTER,
        sdl2.SDLK_TAB:        window.key.TAB }

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
    """ Set gl configuration """

    sdl2.SDL_GL_SetAttribute( sdl2.SDL_GL_RED_SIZE, config.red_size)
    sdl2.SDL_GL_SetAttribute( sdl2.SDL_GL_GREEN_SIZE, config.green_size)
    sdl2.SDL_GL_SetAttribute( sdl2.SDL_GL_BLUE_SIZE, config.blue_size)
    sdl2.SDL_GL_SetAttribute( sdl2.SDL_GL_ALPHA_SIZE, config.alpha_size)
    sdl2.SDL_GL_SetAttribute( sdl2.SDL_GL_DEPTH_SIZE, config.depth_size)
    sdl2.SDL_GL_SetAttribute( sdl2.SDL_GL_STENCIL_SIZE, config.stencil_size)
    if config.samples:
        sdl2.SDL_GL_SetAttribute( sdl2.SDL_GL_MULTISAMPLEBUFFERS, 1)
        sdl2.SDL_GL_SetAttribute( sdl2.SDL_GL_MULTISAMPLESAMPLES, config.samples)
    else:
        sdl2.SDL_GL_SetAttribute( sdl2.SDL_GL_MULTISAMPLEBUFFERS, 0)
        sdl2.SDL_GL_SetAttribute( sdl2.SDL_GL_MULTISAMPLESAMPLES, 0)
    sdl2.SDL_GL_SetAttribute( sdl2.SDL_GL_STEREO, config.stereo)
    sdl2.SDL_GL_SetAttribute( sdl2.SDL_GL_FRAMEBUFFER_SRGB_CAPABLE, config.srgb)
    sdl2.SDL_GL_SetAttribute( sdl2.SDL_GL_CONTEXT_MAJOR_VERSION,
                              config.major_version)
    sdl2.SDL_GL_SetAttribute( sdl2.SDL_GL_CONTEXT_MINOR_VERSION,
                              config.minor_version)
    if config.profile == "core":
        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_PROFILE_MASK,
                                 sdl2.SDL_GL_CONTEXT_PROFILE_CORE)
    elif config.profile == "compatibility":
        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_PROFILE_MASK,
                                 sdl2.SDL_GL_CONTEXT_PROFILE_COMPATIBILITY)
#    elif configuration.profile == "es":
#        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONFIGURATION_PROFILE_MASK,
#                                 sdl2.SDL_GL_CONFIGURATION_PROFILE_ES)



# ------------------------------------------------------------------ Window ---
class Window(window.Window):
    """ """

    def __init__( self, width=256, height=256, title=None, visible=True, aspect=None,
                  decoration=True, fullscreen=False, config=None, context=None, color=(0,0,0,1)):
        """ """

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

        flags  = sdl2.SDL_WINDOW_SHOWN
        # flags |= sdl2.SDL_WINDOW_ALLOW_HIGHDPI
        flags |= sdl2.SDL_WINDOW_RESIZABLE
        flags |= sdl2.SDL_WINDOW_OPENGL
        if visible:
            flags |= sdl2.SDL_WINDOW_SHOWN
        else:
            flags |= SDL_WINDOW_HIDDEN
        if not decoration:
            flags |= sdl2.SDL_WINDOW_BORDERLESS

        self._native_window = sdl2.SDL_CreateWindow(self._title,
                                                    sdl2.SDL_WINDOWPOS_UNDEFINED,
                                                    sdl2.SDL_WINDOWPOS_UNDEFINED,
                                                    width, height, flags)
        self._native_context = sdl2.SDL_GL_CreateContext(self._native_window)
        self._native_id = sdl2.SDL_GetWindowID(self._native_window)
        sdl2.SDL_GL_SetSwapInterval(0)

        # OSX: check framebuffer size / window size. On retina display, they
        #      can be different so we try to correct window size such as having
        #      the framebuffer size of the right size
        # w,h = ctypes.c_int(),ctypes.c_int()
        # sdl2.SDL_GL_GetDrawableSize(self._native_window, w, h)
        # w,h = w.value(), h.value()
        # if w != width or h!= height:
        #     width = width/2
        #     height= height/2
        #     sdl2.SDL_SetWindowSize(self._native_window, int(width), int(height))

        self._height = height
        self._width = width
        __windows__[self._native_id] = self


    def process_event(self, event):

        if event.type == sdl2.SDL_WINDOWEVENT:

            if event.window.event == sdl2.SDL_WINDOWEVENT_RESIZED:
                width = event.window.data1
                height = event.window.data2
                self.dispatch_event('on_resize', width, height)
            elif event.window.event == sdl2.SDL_WINDOWEVENT_SHOWN:
                self.dispatch_event('on_show')
            elif event.window.event == sdl2.SDL_WINDOWEVENT_HIDDEN:
                self.dispatch_event('on_hide')
            elif event.window.event == sdl2.SDL_WINDOWEVENT_ENTER:
                self.dispatch_event('on_enter')
            elif event.window.event == sdl2.SDL_WINDOWEVENT_LEAVE:
                self.dispatch_event('on_leave')
            #elif event.window.event == sdl2.SDL_WINDOWEVENT_MOVED:
            #    self.dispatch_event('on_move')
            elif event.window.event == sdl2.SDL_WINDOWEVENT_CLOSE:
                self.close()

        elif event.type == sdl2.SDL_QUIT:
            self.close()

        elif event.type == sdl2.SDL_MOUSEMOTION:
            x = event.motion.x
            y = event.motion.y
            buttons = event.motion.state
            dx = x - self._mouse_x
            dy = y - self._mouse_y
            self._mouse_x = x
            self._mouse_y = y
            if buttons & sdl2.SDL_BUTTON_LMASK:
                self.dispatch_event("on_mouse_drag", x, y, dx, dy, window.mouse.LEFT)
            elif buttons & sdl2.SDL_BUTTON_MMASK:
                self.dispatch_event("on_mouse_drag", x, y, dx, dy, window.mouse.MIDDLE)
            elif buttons & sdl2.SDL_BUTTON_RMASK:
                self.dispatch_event("on_mouse_drag", x, y, dx, dy, window.mouse.RIGHT)
            else:
                self.dispatch_event("on_mouse_motion", x, y, dx, dy)

        elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
            x = event.button.x
            y = event.button.y
            button = event.button.button
            self._mouse_x = x
            self._mouse_y = y
            if button == sdl2.SDL_BUTTON_LEFT:
                self.dispatch_event("on_mouse_press", x, y, window.mouse.LEFT)
            elif button == sdl2.SDL_BUTTON_MIDDLE:
                self.dispatch_event("on_mouse_press", x, y, window.mouse.MIDDLE)
            elif button == sdl2.SDL_BUTTON_RIGHT:
                self.dispatch_event("on_mouse_press", x, y, window.mouse.RIGHT)

        elif event.type == sdl2.SDL_MOUSEBUTTONUP:
            x = event.button.x
            y = event.button.y
            button = event.button.button
            self._mouse_x = x
            self._mouse_y = y
            if button == sdl2.SDL_BUTTON_LEFT:
                self.dispatch_event("on_mouse_release", x, y, window.mouse.LEFT)
            elif button == sdl2.SDL_BUTTON_MIDDLE:
                self.dispatch_event("on_mouse_release", x, y, window.mouse.MIDDLE)
            elif button == sdl2.SDL_BUTTON_RIGHT:
                self.dispatch_event("on_mouse_release", x, y, window.mouse.RIGHT)

        elif event.type == sdl2.SDL_MOUSEWHEEL:
            offset_x = event.wheel.x
            offset_y = event.wheel.y
            self.dispatch_event("on_mouse_scroll",
                                self._mouse_x, self._mouse_y, offset_x, offset_y)

        elif event.type == sdl2.SDL_KEYUP:
            keysym = event.key.keysym
            modifiers = self._modifiers_translate(keysym.mod)
            symbol = self._keyboard_translate(keysym.sym)
            self.dispatch_event("on_key_press", symbol, modifiers)

        elif event.type == sdl2.SDL_KEYDOWN:
            keysym = event.key.keysym
            modifiers = self._modifiers_translate(keysym.mod)
            symbol = self._keyboard_translate(keysym.sym)
            self.dispatch_event("on_key_release", symbol, modifiers)


    def _modifiers_translate( self, modifiers ):
        _modifiers = 0
        if modifiers & (sdl2.SDLK_LSHIFT | sdl2.SDLK_RSHIFT):
            _modifiers |= window.key.MOD_SHIFT
        if modifiers & (sdl2.SDLK_LCTRL | sdl2.SDLK_RCTRL):
            _modifiers |= window.key.MOD_CTRL
        if modifiers & (sdl2.SDLK_LALT | sdl2.SDLK_RALT):
            _modifiers |= window.key.MOD_ALT
        return _modifiers

    def _keyboard_translate(self, code):
        ascii = code
        if (0x020 <= ascii <= 0x040) or (0x05b <= ascii <= 0x07e):
            return ascii
        elif ascii <= 0x020:
            code = ascii
        return __key_map__.get(code, window.key.UNKNOWN)


    def show(self):
        sdl2.SDL_ShowWindow(self._native_window)
        self.dispatch_event('on_show')

    def hide(self):
        sdl2.SDL_HideWindow(self._native_window)
        self.dispatch_event('on_hide')

    def close(self):
        sdl2.SDL_DestroyWindow(self._native_window)
        del __windows__[self._native_id]
        for i in range(len(self._timer_stack)):
            handler, interval = self._timer_stack[i]
            self._clock.unschedule(handler)
        self.dispatch_event('on_close')

    def set_title(self, title):
        log.warn('%s backend cannot set window title' % __name__)

    def get_title(self):
        log.warn('%s backend cannot get window title' % __name__)

    def set_size(self, width, height):
        log.warn('%s backend cannot set window size' % __name__)

    def get_size(self):
        log.warn('%s backend cannot get window size' % __name__)

    def set_position(self, x, y):
        log.warn('%s backend cannot set window position' % __name__)

    def get_position(self):
        log.warn('%s backend cannot get position' % __name__)

    def swap(self):
        sdl2.SDL_GL_SwapWindow(self._native_window)

    def activate(self):
        sdl2.SDL_GL_MakeCurrent(self._native_window, self._native_context)



# ----------------------------------------------------------------- windows ---
def windows():
    return __windows__.values()


# ----------------------------------------------------------------- process ---
def process(dt):

    # Poll for and process events
    event = sdl2.SDL_Event()
    while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
        win_id = event.window.windowID
        if win_id in __windows__.keys():
            win = __windows__[win_id]
            win.process_event(event)

    for window in windows():
        # Make window active
        window.activate()

        # Dispatch the main draw event
        window.dispatch_event('on_draw', dt)

        # Dispatch the idle event
        window.dispatch_event('on_idle', dt)

        # Swap buffers
        window.swap()

    return len(__windows__.values())
