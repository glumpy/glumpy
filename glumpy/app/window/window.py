# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import sys
from glumpy import gl
from glumpy.log import log
from glumpy.app import configuration
from . import key
from . import mouse
from . import event


class Window(event.EventDispatcher):
    """
    Platform independent window.

    :param int width:
      Initial width (pixels)

    :param int height:
      Initial height (pixels)

    :param strtitle:
       Window title

    :param bool visible:
       Initial visibility status

    :param bool decoration:
       Whether window is decorated

    :param bool fullscreen:
       Initial fullscreen status

    :param config:
       GL Configuration

    :param Window context:
       Window to share GL context with

    :param 4-tuple color:
       Clear color


    The content area of a window is filled entirely with an OpenGL viewport.
    Applications have no access to operating system widgets or controls; all
    rendering must be done via OpenGL.

    Windows may appear as floating regions or can be set to fill an entire
    screen (fullscreen).  When floating, windows may appear borderless or
    decorated with a platform-specific frame (including, for example, the
    title bar, minimize and close buttons, resize handles, and so on).

    While it is possible to set the location of a window, it is recommended
    that applications allow the platform to place it according to local
    conventions.  This will ensure it is not obscured by other windows,
    and appears on an appropriate screen for the user.

    It is the responsability of the window backend to dispatch the following
    events when necessary:

    **Keyboard**::

      def on_key_press(symbol, modifiers):
          'A key on the keyboard was pressed.'
          pass

      def on_key_release(symbol, modifiers):
          'A key on the keyboard was released.'
          pass

      def on_character(text):
          'A character has been typed'
          pass

    **Mouse**::

      def on_mouse_press(self, x, y, button):
          'A mouse button was pressed.'
          pass

      def on_mouse_release(self, x, y, button):
          'A mouse button was released.'
          pass

      def on_mouse_motion(x, y, dx, dy):
          'The mouse was moved with no buttons held down.'
          pass

      def on_mouse_drag(x, y, dx, dy, buttons):
          'The mouse was moved with some buttons pressed.'
          pass

      def on_mouse_scroll(self, dx, dy):
          'The mouse wheel was scrolled by (dx,dy).'
          pass


    **Window**::

      def on_init(self):
          'The window has just initialized iself.'
          pass

      def on_show(self):
          'The window was shown.'
          pass

      def on_hide(self):
          'The window was hidden.'
          pass

      def on_close(self):
          'The user closed the window.'
          pass

      def on_resize(self, width, height):
          'The window was resized to (width,height)'
          pass

      def on_draw(self, dt):
          'The window contents must be redrawn.'
          pass

      def on_idle(self, dt):
          'The window is inactive.'
          pass

    """

    def __init__(self, width=256, height=256, title=None, visible=True, aspect=None,
                 decoration=True, fullscreen=False, config=None, context=None, color=(0,0,0,1)):
        """
        Create a window.
        """

        event.EventDispatcher.__init__(self)
        self._mouse_x = 0
        self._mouse_y = 0
        self._button = mouse.NONE
        self._x = 0
        self._y = 0
        self._width = width
        self._height = height
        self._title = (title or sys.argv[0])
        self._visible = visible
        self._fullscreen = fullscreen
        self._decoration = decoration
        self._clock = None
        self._timer_stack = []
        self._timer_date = []
        self._backend = None
        self._color = color

        self._clearflags = gl.GL_COLOR_BUFFER_BIT
        if config._depth_size:
            self._clearflags |= gl.GL_DEPTH_BUFFER_BIT
        if config._stencil_size:
            self._clearflags |= gl.GL_STENCIL_BUFFER_BIT


    @property
    def width(self):
        """ Window width (pixels, read-only) """

        return self._width

    
    @property
    def height(self):
        """ Window height (pixels, read-only) """

        return self._height

    @property
    def fps(self):
        """ Frame per second (read-only). """

        return self._clock.get_fps()

    
    @property
    def config(self):
        return self._config

    @property
    def color(self):
        """ Window clear color (read/write) """
        
        return self._color

    
    @color.setter
    def color(self, color):
        self._color = color
        gl.glClearColor(*self._color)

        
    def clear(self,color=None, clearflags=None):
        """ Clear the whole window """

        if color is not None:
            gl.glClearColor(*color)
            if  clearflags is not None: gl.glClear(clearflags)
            else:                       gl.glClear(self._clearflags)
        else:
            gl.glClearColor(*self._color)
            if  clearflags is not None: gl.glClear(clearflags)
            else:                       gl.glClear(self._clearflags)

    def on_init(self):
        """ Window initialization """

        gl.glClearColor(*self._color)


    def on_resize(self, width, height):
        """" Default resize handler that set viewport """
        gl.glViewport(0, 0, width, height)
        self.dispatch_event('on_draw', 0.0)
        self.swap()

    def on_key_press(self, k, modifiers):
        """" Default key handler that close window on escape """
        if k == key.ESCAPE:
            self.close()
            return True
        elif k == key.F10:
            import os, sys
            import numpy as np
            from glumpy.ext import png
            framebuffer = np.zeros((self.height, self.width * 3), dtype=np.uint8)
            gl.glReadPixels(0, 0, self.width, self.height,
                            gl.GL_RGB, gl.GL_UNSIGNED_BYTE, framebuffer)

            basename = os.path.basename(os.path.realpath(sys.argv[0]))
            dirname = os.path.dirname(os.path.realpath(sys.argv[0]))
            basename = '.'.join(basename.split('.')[:-1])
            filename = os.path.join(dirname,"%s.png" % basename)
            png.from_array(framebuffer[::-1], 'RGB').save(filename)
#            index = 0
#            filename = "%s-%04d.png" % (basename,index)
#            while os.path.exists(os.path.join(dirname, filename)):
#                index += 1
#                filename = "%s-%04d.png" % (basename, index)
#            png.from_array(framebuffer, 'RGB').save(filename)
            return True

    def show(self):
        """ Make the window visible """
        log.warn('%s backend cannot show window' % self._backend.name())

    def hide(self):
        """ Hide the window """
        log.warn('%s backend cannot hide window' % self._backend.name())

    def close(self):
        """ Close (destroy) the window """
        log.warn('%s backend cannot close window' % self._backend.name())

    def set_title(self, title):
        """ Set window title """
        log.warn('%s backend cannot set window title' % self._backend.name())

    def get_title(self):
        """ Get window title """
        log.warn('%s backend cannot get window title' % self._backend.name())

    def set_size(self, width, height):
        """ Set window size """
        log.warn('%s backend cannot set window size' % self._backend.name())

    def get_size(self):
        """ Get window size """
        log.warn('%s backend cannot get window size' %  self._backend.name())

    def set_position(self, x, y):
        """ Set window position """
        log.warn('%s backend cannot set window position' %  self._backend.name())

    def get_position(self):
        """ Get window position """
        log.warn('%s backend cannot get position' %  self._backend.name())

    def set_fullscreen(self, fullsrceen):
        """ Set window fullscreen mode """
        log.warn('%s backend cannot set fullscreen mode' % self._backend.name())

    def get_fullscreen(self):
        """ Get window fullscreen mode """
        log.warn('%s backend cannot get fullscreen mode' % self._backend.name())

    def swap(self):
        """ Swap GL buffers """
        log.warn('%s backend cannot swap buffers' % self._backend.name())

    def activate(self):
        """ Activate window """
        log.warn('%s backend cannot make window active' % self._backend.name())

    def timer(self, delay):
        """Function decorator for timed handlers.

        :Parameters:

            ``delay``: int
                Delay in second

        Usage::

            window = window.Window()

            @window.timer(0.1)
            def timer(dt):
                do_something ...
        """

        def decorator(func):
            self._timer_stack.append((func, delay))
            self._timer_date.append(0)
            return func
        return decorator



Window.register_event_type('on_enter')
Window.register_event_type('on_leave')
Window.register_event_type('on_draw')
Window.register_event_type('on_resize')
Window.register_event_type('on_mouse_motion')
Window.register_event_type('on_mouse_drag')
Window.register_event_type('on_mouse_press')
Window.register_event_type('on_mouse_release')
Window.register_event_type('on_mouse_scroll')
Window.register_event_type('on_character')
Window.register_event_type('on_key_press')
Window.register_event_type('on_key_release')
Window.register_event_type('on_init')
Window.register_event_type('on_show')
Window.register_event_type('on_hide')
Window.register_event_type('on_close')
Window.register_event_type('on_idle')
