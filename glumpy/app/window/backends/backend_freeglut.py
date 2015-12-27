# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
"""
`FreeGLUT <http://freeglut.sourceforge.net>`_ is a free-software/open-source
alternative to the OpenGL Utility Toolkit (GLUT) library. GLUT was originally
written by Mark Kilgard to support the sample programs in the second edition
OpenGL RedBook. Since then, GLUT has been used in a wide variety of practical
applications because it is simple, widely available and highly portable.

**Usage**

  .. code:: python

     from glumpy import app

     app.use("freeglut")
     window = app.Window()


**Capability**

========================== ======== ======================== ========
Multiple windows              ✘     Set GL API                  ✘
-------------------------- -------- ------------------------ --------
Non-decorated windows         ✓     Set GL Profile              ✘
-------------------------- -------- ------------------------ --------
Resize windows                ✓     Share GL Context            ✘
-------------------------- -------- ------------------------ --------
Move windows                  ✓     Unicode handling            ✘
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
__name__ = "FreeGLUT"

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
        glut.glutInit(sys.argv)
    __initialized__ = True

def __exit__():
    global __initialized__
    # Not an error, we cannot really terminate glut
    __initialized__ = True


# ------------------------------------------------------------ availability ---
try:
    import sys
    import OpenGL.GLUT as glut
    if sys.platform == 'darwin':
        import OpenGL.platform as platform
        try:
            glutCheckLoop = platform.createBaseFunction(
                'glutCheckLoop', dll=platform.GLUT, resultType=None,
                argTypes=[], doc='glutCheckLoop( ) -> None', argNames=(), )
        except AttributeError:
            __availability__ = False
            __version__ = None
        __availability__ = True
        __version__ = "%d" % glut.GLUT_API_VERSION
        __init__()

        __mouse_map__ = { glut.GLUT_LEFT_BUTTON:   window.mouse.LEFT,
                          glut.GLUT_MIDDLE_BUTTON: window.mouse.MIDDLE,
                          glut.GLUT_RIGHT_BUTTON:  window.mouse.RIGHT }

        __key_map__   = { 0x008:                   window.key.BACKSPACE,
                          0x009:                   window.key.TAB,
                          0x00A:                   window.key.LINEFEED,
                          0x00C:                   window.key.CLEAR,
                          0x00D:                   window.key.RETURN,
                          0x018:                   window.key.CANCEL,
                          0x01B:                   window.key.ESCAPE,
                          glut.GLUT_KEY_F1:        window.key.F1,
                          glut.GLUT_KEY_F2:        window.key.F2,
                          glut.GLUT_KEY_F3:        window.key.F3,
                          glut.GLUT_KEY_F4:        window.key.F4,
                          glut.GLUT_KEY_F5:        window.key.F5,
                          glut.GLUT_KEY_F6:        window.key.F6,
                          glut.GLUT_KEY_F7:        window.key.F7,
                          glut.GLUT_KEY_F8:        window.key.F8,
                          glut.GLUT_KEY_F9:        window.key.F9,
                          glut.GLUT_KEY_F10:       window.key.F10,
                          glut.GLUT_KEY_F11:       window.key.F11,
                          glut.GLUT_KEY_F12:       window.key.F12,
                          glut.GLUT_KEY_LEFT:      window.key.LEFT,
                          glut.GLUT_KEY_UP:        window.key.UP,
                          glut.GLUT_KEY_RIGHT:     window.key.RIGHT,
                          glut.GLUT_KEY_DOWN:      window.key.DOWN,
                          glut.GLUT_KEY_PAGE_UP:   window.key.PAGEUP,
                          glut.GLUT_KEY_PAGE_DOWN: window.key.PAGEDOWN,
                          glut.GLUT_KEY_HOME:      window.key.HOME,
                          glut.GLUT_KEY_END:       window.key.END,
                          glut.GLUT_KEY_INSERT:    window.key.INSERT }
    else:
        __availability__ = False
        __version__ = None
except ImportError:
    __availability__ = False
    __version__ = None


# -------------------------------------------------------------- capability ---
capability = {
    "Window position get/set" : True,
    "Window size get/set"     : True,
    "Multiple windows"        : False,
    "Mouse scroll events"     : False,
    "Non-decorated window"    : True,
    "Non-sizeable window"     : False,
    "Fullscreen mode"         : True,
    "Unicode processing"      : False,
    "Set GL version"          : False,
    "Set GL profile"          : False,
    "Share GL context"        : False,
}




# ------------------------------------------------------- set_configuration ---
def set_configuration(config):
    """ Set gl configuration """

    s = ""
    s += "acca=0 " # No accum buffer
    s += "red>=%d " % config.red_size
    s += "green>=%d " % config.green_size
    s += "blue>=%d " % config.blue_size
    s += "alpha>=%d " % config.alpha_size
    s += "depth>=%d " % config.depth_size
    s += "stencil~%d " % config.stencil_size
    if config.double_buffer:
        s += "double=1 "
    else:
        s += "single=1 "
    s += "stereo=%d " % config.stereo
    s += "samples~%d " % config.samples

    glut.glutInitDisplayString(s)



# ------------------------------------------------------------------ Window ---
class Window(window.Window):

    def __init__( self, width=256, height=256, title=None, visible=True, aspect=None,
                  decoration=True, fullscreen=False, config=None, context=None, color=(0,0,0,1)):

        if len(__windows__) > 0:
            log.critical(
                """OSXGLUT backend is unstable with more than one window.\n"""
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

        self._native_window = glut.glutCreateWindow( self._title )
        if bool(glut.glutSetOption):
            glut.glutSetOption(glut.GLUT_ACTION_ON_WINDOW_CLOSE,
                               glut.GLUT_ACTION_CONTINUE_EXECUTION)
            glut.glutSetOption(glut.GLUT_ACTION_GLUTMAINLOOP_RETURNS,
                               glut.GLUT_ACTION_CONTINUE_EXECUTION)
        glut.glutWMCloseFunc( self._close )
        glut.glutDisplayFunc( self._display )
        glut.glutReshapeFunc( self._reshape )
        glut.glutKeyboardFunc( self._keyboard )
        glut.glutKeyboardUpFunc( self._keyboard_up )
        glut.glutMouseFunc( self._mouse )
        glut.glutMotionFunc( self._motion )
        glut.glutPassiveMotionFunc( self._passive_motion )
        glut.glutVisibilityFunc( self._visibility )
        glut.glutEntryFunc( self._entry )
        glut.glutSpecialFunc( self._special )
        glut.glutSpecialUpFunc( self._special_up )
        glut.glutReshapeWindow( self._width, self._height )
        if visible:
            glut.glutShowWindow()
        else:
            glut.glutHideWindow()

        # This ensures glutCheckLoop never blocks
        def on_idle(): pass
        glut.glutIdleFunc(on_idle)

        __windows__.append(self)


    def _keyboard( self, code, x, y ):
        symbol = self._keyboard_translate(code)
        modifiers = glut.glutGetModifiers()
        modifiers = self._modifiers_translate(modifiers)
        self.dispatch_event('on_key_press', symbol, modifiers)

    def _keyboard_up( self, code, x, y ):
        modifiers = glut.glutGetModifiers()
        self.dispatch_event('on_key_release',
                            self._keyboard_translate(code),
                            self._modifiers_translate(modifiers))

    def _special( self, code, x, y ):
        modifiers = glut.glutGetModifiers()
        self.dispatch_event('on_key_press',
                            self._keyboard_translate(code),
                            self._modifiers_translate(modifiers))

    def _special_up( self, code, x, y ):
        modifiers = glut.glutGetModifiers()
        self.dispatch_event('on_key_release',
                            self._keyboard_translate(code),
                            self._modifiers_translate(modifiers))


    def _modifiers_translate( self, modifiers ):
        _modifiers = 0
        if modifiers & glut.GLUT_ACTIVE_SHIFT:
            _modifiers |=  window.key.MOD_SHIFT
        if modifiers & glut.GLUT_ACTIVE_CTRL:
            _modifiers |=  window.key.MOD_CTRL
        if modifiers & glut.GLUT_ACTIVE_ALT:
            _modifiers |=  window.key.MOD_ALT
        return _modifiers


    def _keyboard_translate( self, code ):
        ascii = ord(code.lower())
        if (0x020 <= ascii <= 0x040) or (0x05b <= ascii <= 0x07e):
            return ascii
        elif ascii <= 0x020:
            code = ascii
        return __key_map__.get(code, window.key.UNKNOWN)


    def _display( self ):
        pass

    def _close( self ):
        __windows__.remove(self)
        # WARNING: This does not work on OSX 10.9 (seg fault or bus error)
        # glut.glutDestroyWindow(self._native_window)
        glut.glutSetWindow(self._native_window)
        glut.glutHideWindow()
        for i in range(len(self._timer_stack)):
            handler, interval = self._timer_stack[i]
            self._clock.unschedule(handler)
        self.dispatch_event('on_close')

    def _reshape(self, width, height):
        self._width  = glut.glutGet(glut.GLUT_WINDOW_WIDTH)
        self._height = glut.glutGet(glut.GLUT_WINDOW_HEIGHT)
        self.dispatch_event('on_resize', self._width, self._height)

    def _visibility(self, state):
        if state == glut.GLUT_VISIBLE:
            self.dispatch_event('on_show')
        elif state == glut.GLUT_NOT_VISIBLE:
            self.dispatch_event('on_hide')

    def _entry(self, state):
        if state == glut.GLUT_ENTERED:
            self.dispatch_event('on_enter')
        elif state == glut.GLUT_LEFT:
            self.dispatch_event('on_leave')


    def _mouse(self, button, state, x, y):
        button = __mouse_map__.get(button, window.mouse.UNKNOWN)
        if state == glut.GLUT_UP:
            self._button = 0
            self._mouse_x = x
            self._mouse_y = y
            self.dispatch_event('on_mouse_release', x, y, button)
        elif state == glut.GLUT_DOWN:
            self._button = button
            self._mouse_x = x
            self._mouse_y = y
            if button == 3:
                self._button = 0
                self.dispatch_event('on_mouse_scroll', x, y, 0, 1)
            elif button == 4:
                self._button = 0
                self.dispatch_event('on_mouse_scroll', x, y, 0, -1)
            else:
                self.dispatch_event('on_mouse_press', x, y, button)

    def _motion(self, x, y):
        dx = x - self._mouse_x
        dy = y - self._mouse_y
        self._mouse_x = x
        self._mouse_y = y
        self.dispatch_event('on_mouse_drag', x, y, dx, dy, self._button)


    def _passive_motion(self, x, y):
        dx = x - self._mouse_x
        dy = y - self._mouse_y
        self._mouse_x = x
        self._mouse_y = y
        self.dispatch_event('on_mouse_motion', x, y, dx, dy)


    def close(self):
        self._close()

    def show(self):
        self.activate()
        glut.glutShowWindow()
        self.dispatch_event('on_show')


    def hide(self):
        self.activate()
        glut.glutHideWindow()
        self.dispatch_event('on_hide')


    def set_title(self, title):
        self.activate()
        glut.glutSetWindowTitle( title )
        self._title = title

    def get_title(self, title):
        return self._title

    def set_size(self, width, height):
        self.activate()
        glut.glutReshapeWindow(width, height)

    def get_size(self):
        self.activate()
        self._width  = glut.glutGet( glut.GLUT_WINDOW_WIDTH )
        self._height = glut.glutGet( glut.GLUT_WINDOW_HEIGHT )
        return self._width, self._height

    def set_position(self, x, y):
        glut.glutPositionWindow( x, y )


    def get_position(self):
        glut.glutSetWindow( self._native_window )
        self._x = glut.glutGet( glut.GLUT_WINDOW_W )
        self._y = glut.glutGet( glut.GLUT_WINDOW_Y )
        return self._x, self._y

    def swap(self):
        glut.glutSwapBuffers()

    def activate(self):
        glut.glutSetWindow(self._native_window)


# ----------------------------------------------------------------- windows ---
def windows():
    return __windows__


# ----------------------------------------------------------------- process ---
def process(dt):

    # Poll for and process events
    glut.glutMainLoopEvent()

    for window in __windows__:
        window.activate()

        # Dispatch the main draw event
        window.dispatch_event('on_draw', dt)

        # Dispatch the idle event
        window.dispatch_event('on_idle', dt)

        # Swap buffers
        window.swap()

    return len(__windows__)
