# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
"""
"""
from . window import event
from glumpy.log import log
from glumpy import gloo, gl, library

class ViewportDispatcher(event.EventDispatcher):
    def __init__(self):
        pass

ViewportDispatcher.register_event_type('on_enter')
ViewportDispatcher.register_event_type('on_leave')
ViewportDispatcher.register_event_type('on_resize')
ViewportDispatcher.register_event_type('on_mouse_motion')
ViewportDispatcher.register_event_type('on_mouse_drag')
ViewportDispatcher.register_event_type('on_mouse_press')
ViewportDispatcher.register_event_type('on_mouse_release')
ViewportDispatcher.register_event_type('on_mouse_scroll')
ViewportDispatcher.register_event_type('on_character')
ViewportDispatcher.register_event_type('on_key_press')
ViewportDispatcher.register_event_type('on_key_release')
ViewportDispatcher.register_event_type('on_draw')


class Viewport(event.EventDispatcher):
    """
    A Viewport represents a rectangular area on a window.

    :param size: Requested size as (width, height)
    :param position:  Requested position as (x,y)
    :param anchor: Anchor point as (x,y)
    :param float aspect: Aspect (= width/height).

    The size and the position are always relative to the parent viewport.  They
    may be given in pixels (int) or as a percentage (float) of parent viewport
    size. Positive or negative values are accepted.

    .. important::
    
       The viewport class works in conjunction with the Viewport transform that
       ensure actual positioning and sizing within a shader program.

    Let's consider a root viewport of size 400x400 and a child viewport:

    **Absolute size**

      .. code:: python

         viewport = Viewport(400,400)
         child = Viewport(100,100)
         viewport.add(child)

         # Child size is 100x100 (pixels)

      .. code:: python

         viewport = Viewport(400,400)
         child = Viewport(-100, -100)
         viewport.add(child)

         # Child size is (400-100) x (400-100) = 300 x 300 (pixels)


    **Relative size**

      .. code:: python

         viewport = Viewport(400,400)
         child = Viewport(0.5, 0.5)
         viewport.add(child)

         # Child size is 400*0.5 x 400*0.5 = 200 x 200 (pixels)

         # Child size is 200x200 pixels.

      .. code:: python

         viewport = Viewport(400,400)
         child = Viewport(-0.125, -0.125)
         viewport.add(child)

         # Child size is (400*(1-0.125)) x (400*(1-0.125)) = 50 x 50 (pixels)

      .. note::

         It is also possible to define an aspect (width/height) that will be
         enforced anytime.

    Positioning the viewport inside the parent viewport is also made using
    absolute or relative coordinates.

    **Absolute position**

      .. code:: python

         viewport = Viewport(size=(400,400), position=(0,0))
         child = Viewport(size=(100,100), position=(10,10))
         viewport.add(child)

         # Child position is +10+10 (pixels)

      .. code:: python

         viewport = Viewport(size=(400,400), position=(0,0))
         child = Viewport(size=(100,100), position=(-10,-10))
         viewport.add(child)

         # Child position is +(400-10)+(400-10) = +390+390 (pixels)

    **Relative position**

      .. code:: python

         viewport = Viewport(size=(400,400), position=(0,0))
         child = Viewport(size=(100,100), position=(0.25,0.25))
         viewport.add(child)

         # Child position is +(400*0.25)+(400*0.25) = +100+100 (pixels)

      .. code:: python

         viewport = Viewport(size=(400,400), position=(0,0))
         child = Viewport(size=(100,100), position=(-0.25,-0.25))
         viewport.add(child)

         # Child position is +(400*(1-0.25))+(400*(1-0.25)) = +300+300 (pixels)

      .. note::

         The final position of the viewport relates to the anchor point which
         can be also set in absolute or relative coordinates.

    The order of rendering is done according to the order of the viewport
    hierarchy, starting from the root viewport.
    """


    # Internal id counter to keep track of created objects
    _idcount = 0


    def __init__(self, size=(800,600), position=(0,0), anchor=(0,0), aspect=None):
        """
        Create a new viewport with requested size and position.

        Parameters
        ----------
        """

        self._parent = None
        self._children = []
        self._active_viewports = []
        self._dispatcher = ViewportDispatcher()

        # Aspect ratio (width/height)
        self._aspect = aspect
        if aspect:
            log.info("Enforcing viewport aspect ratio (%g)" % aspect)

        # Anchor point for placement
        self._anchor = anchor

        # Requested size & position (may be honored or not, depending on parent)
        # (relative or absolute coordinates)
        self._requested_size     = size
        self._requested_position = position

        # Clipped size & position (used for glScissor)
        # (absolute coordinates)
        self._scissor_size     = size
        self._scissor_position = position

        # Viewport size & position (used for glViewport)
        # (absolute coordinates)
        self._viewport_size     = size
        self._viewport_position = position

        # Wheter viewport is active (cursor is inside)
        self._active = False

        # Viewport id
        self._id = Viewport._idcount
        Viewport._idcount += 1


    def event(self, *args):
        return self._dispatcher.event(*args)

    def attach(self, *args, **kwargs):
        self.dispatcher.push_handlers(*args, **kwargs)


    def add(self, child):
        """ Add a new child to the viewport """

        child._parent = self
        self._children.append(child)


    def __getitem__(self, index):
        """Get children using index"""

        return self._children[index]

    @property
    def dispatcher(self):
        """ Event dispatcher """

        return self._dispatcher

    @property
    def name(self):
        """ Viewport name """

        return "VP%d" % (self._id)


    @property
    def active(self):
        """ Whether viewport is active """

        return self._active


    @active.setter
    def active(self, value):
        """ Whether viewport is active """

        self._active = value
        for child in self._children:
            child.active = value


    @property
    def root(self):
        """ Root viewport """

        if not self._parent:
            return self
        return self._parent.root

    @property
    def parent(self):
        """ Parent viewport """
        return self._parent


    @property
    def extents(self):
        """ Actual position and size of the viewport """

        x,y = self._viewport_position
        w,h = self._viewport_size
        return x, y, w, h


    @property
    def scissor(self):
        """ Actual position and size of the scissor """

        x,y = self._scissor_position
        w,h = self._scissor_size
        return x, y, w, h


    @property
    def size(self):
        """ Actual size of the viewport """

        return self._viewport_size

    @size.setter
    def size(self, size):
        """ Actual size of the viewport """

        self._requested_size = size
        self.root._compute_viewport()


    @property
    def position(self):
        """ Actual position of the viewport """

        return self._viewport_position


    @position.setter
    def position(self, position):
        """ Actual position of the viewport """

        self._requested_position = position
        self.root._compute_viewport()


    def _compute_viewport(self):
        """ Compute actual viewport in absolute coordinates """

        # Root requests are always honored, modulo the aspect
        if self.parent is None:
            w,h = self._requested_size
            if self._aspect:
                h = w * self._aspect
                if h > self._requested_size[1]:
                    h = self._requested_size[1]
                    w = h/self._aspect
            x = (self._requested_size[0] - w)/2
            y = (self._requested_size[1] - h)/2
            self._position          = x,y
            self._size              = w,h
            self._viewport_position = x,y
            self._viewport_size     = w,h
            self._scissor_position  = x,y
            self._scissor_size      = w,h
            for child in self._children:
                child._compute_viewport()
            return

        # Children viewport request depends on parent viewport
        pvx, pvy = self.parent._viewport_position
        pvw, pvh = self.parent._viewport_size
        psx, psy = self.parent._scissor_position
        psw, psh = self.parent._scissor_size

        # Relative width (to actual parent viewport)
        # ------------------------------------------
        if self._requested_size[0] <= -1.0:
            vw = max(pvw + self._requested_size[0],0)
        elif self._requested_size[0] < 0.0:
            vw = max(pvw + self._requested_size[0]*pvw,0)
        elif self._requested_size[0] <= 1.0:
            vw = self._requested_size[0]*pvw
        # Absolute width
        else:
            vw = self._requested_size[0]
        vw = int(round(vw))

        # Enforce aspect first
        if self._aspect:
            vh = self._aspect*vw
            if vh > pvh and -1 < self._requested_size[0] <= 1:
                vh = pvh
                vw = vh/self._aspect



        # Relative height (to actual parent viewport)
        # -------------------------------------------
        else:
            if self._requested_size[1] <= -1.0:
                vh = max(pvh + self._requested_size[1],0)
            elif self._requested_size[1] < 0.0:
                vh = max(pvh + self._requested_size[1]*pvh,0)
            elif self._requested_size[1] <= 1.0:
                vh = self._requested_size[1]*pvh
            # Absolute height
            else:
                vh = self._requested_size[1]
        vh = int(round(vh))

        # X anchor
        # ---------------------------------------
        if self._anchor[0] <= -1.0:
            ax = vw + self._anchor[0]
        elif self._anchor[0] < 0.0:
            ax = vw + self._anchor[0]*vw
        elif self._anchor[0] < 1.0:
            ax = self._anchor[0]*vw
        else:
            ax = self._anchor[0]
        ax = int(round(ax))

        # X positioning
        # ---------------------------------------
        if self._requested_position[0] <= -1.0:
            vx = pvw + self._requested_position[0]
        elif -1.0 < self._requested_position[0] < 0.0:
            vx = pvw + self._requested_position[0]*pvw
        elif 0.0 <= self._requested_position[0] < 1.0:
            vx = self._requested_position[0]*pvw
        else:
            vx = self._requested_position[0]
        vx = int(round(vx)) + pvx - ax

        # Y anchor
        # ---------------------------------------
        if self._anchor[1] <= -1.0:
            ay = vh + self._anchor[1]
        elif -1.0 < self._anchor[1] < 0.0:
            ay = vh + self._anchor[1]*vh
        elif 0.0 <= self._anchor[1] < 1.0:
            ay = self._anchor[1]*vh
        else:
            ay = self._anchor[1]
        ay = int(round(ay))

        # Y positioning
        # ---------------------------------------
        if self._requested_position[1] <= -1.0:
            vy = pvh + self._requested_position[1] #- vh
        elif -1.0 < self._requested_position[1] < 0.0:
            vy = pvh + self._requested_position[1]*pvh

        elif 0.0 <= self._requested_position[1] < 1.0:
            vy = self._requested_position[1]*pvh
        else:
            vy = self._requested_position[1]
        vy = int(round(vy)) + pvy - ay


        # Compute scissor size & position
        sx = max(pvx,vx)
        sy = max(pvy,vy)
        sw = max(min(psw-(sx-pvx)-1,vw), 0)
        sh = max(min(psh-(sy-pvy)-1,vh), 0)

        # Update internal information
        self._viewport_size     = vw, vh
        self._viewport_position = vx, vy
        self._scissor_size      = sw, sh
        self._scissor_position  = sx, sy

        # Update children
        for child in self._children:
            child._compute_viewport()


    def __contains__(self, xy):
        x,y = xy
        # WARN: mouse pointer is usually upside down
        y = self.root.size[1] - y
        xmin = self._viewport_position[0]
        xmax = xmin + self._viewport_size[0]
        ymin = self._viewport_position[1]
        ymax = ymin + self._viewport_size[1]
        return  xmin <= x < xmax and  ymin <= y < ymax

    # def lock(self):
    #     vx, vy = self._viewport_position
    #     vw, vh = self._viewport_size
    #     sx, sy = self._scissor_position
    #     sw, sh = self._scissor_size
    #     gl.glPushAttrib( gl.GL_VIEWPORT_BIT | gl.GL_SCISSOR_BIT )
    #     gl.glViewport( vx, vy, vw, vh )
    #     gl.glEnable( gl.GL_SCISSOR_TEST )
    #     gl.glScissor( sx, sy, sw+1, sh+1 )

    # def unlock(self):
    #     gl.glPopAttrib( )


    def on_draw(self, dt):

        # Root viewport
        if self.parent is None:
            # gl.glEnable(gl.GL_SCISSOR_TEST)
            # gl.glViewport(*self.viewport)
            # gl.glScissor(*self.scissor)

            self.dispatcher.dispatch_event("on_draw", dt)

        for child in self._children:
            # x,y = child._viewport_position
            # w,h = child._viewport_size
            # gl.glViewport(x,y,w,h)
            # x,y = child._scissor_position
            # w,h = child._scissor_size
            # gl.glScissor(x,y,w+1,h+1)

            # WARNING
            # Order is important because the direct 'on_draw' event on child
            # may result in a viewport/scissor modification.
            child.dispatcher.dispatch_event("on_draw", dt)
            child.dispatch_event("on_draw", dt)

        # if self.parent is None:
        #     gl.glDisable(gl.GL_SCISSOR_TEST)
        #     gl.glViewport(*self.viewport)


    def on_resize(self, width, height):
        if self.parent == None:
            self._requested_size = width, height

        self._compute_viewport()
        self.dispatcher.dispatch_event("on_resize", self.size[0], self.size[1])

        for child in self._children:
            child.dispatch_event("on_resize", width, height)



    def on_key_press(self, key, modifiers):
        """ Default key handler that close window on escape """
        pass

        # if key == window.key.ESCAPE:
        #     self.close()
        #     return True

    def on_mouse_press(self, x, y, button):
        self.dispatcher.dispatch_event("on_mouse_press",
                                       x-self.position[0], y-self.position[1], button)
        if self.parent == None:
            self._active_viewports = []

        for child in self._children:
            if (x,y) in child:
                self.root._active_viewports.append(child)
                ox, oy = child.position
                child.dispatch_event("on_mouse_press", x, y, button)


    def on_mouse_release(self, x, y, button):
        self.dispatcher.dispatch_event(
            "on_mouse_release", x-self.position[0], y-self.position[1], button)

        if self.parent == None:
            for child in self._active_viewports:
                ox, oy = child.position
                child.dispatch_event("on_mouse_release", x, y, button)


    def on_mouse_drag(self, x, y, dx, dy, button):
        self.dispatcher.dispatch_event(
            "on_mouse_drag", x-self.position[0], y-self.position[1], dx, dy, button)

        if self.parent == None:
            if len(self.root._active_viewports):
                #child = self.root._active_viewports[-1]
                for child in self.root._active_viewports:
                    ox, oy = child.position
                    child.dispatch_event("on_mouse_drag", x, y, dx, dy, button)


    def on_mouse_scroll(self, x, y, dx, dy):
        self.dispatcher.dispatch_event(
            "on_mouse_scroll", x-self.position[0], y-self.position[1], dx, dy)

        if self.parent == None:
            if self.root._active_viewports:
                # child = self.root._active_viewports[-1]
                for child in self.root._active_viewports:
                    ox, oy = child.position
                    child.dispatch_event("on_mouse_scroll", x, y, dx, dy)


    def on_mouse_motion(self, x, y, dx, dy):
        self.dispatcher.dispatch_event(
            "on_mouse_motion", x-self.position[0], y-self.position[1], dx, dy)

        for child in self._children:
            ox, oy = child.position
            if (x,y) in child:
                if not child._active:
                    child.dispatch_event("on_enter")
                    child.dispatcher.dispatch_event("on_enter")
                self.active = False
                child._active = True
                child.dispatch_event("on_mouse_motion", x, y, dx, dy)
            else:
                if child._active:
                    child.dispatch_event("on_leave")
                child.active = False
                if (x,y) in self:
                    self._active = True


    def __replines__(self):
        """ ASCII display of trees by Andrew Cooke """
        yield "%s (%dx%d%+d%+d)" % (self.name,
                                    self.size[0], self.size[1],
                                    self.position[0], self.position[1])
        last = self._children[-1] if self._children else None
        for child in self._children:
            prefix = '└── ' if child is last else '├── '
            for line in child.__replines__():
                yield prefix + line
                prefix = '    ' if child is last else '│   '

    def __str__(self):
        return '\n'.join(self.__replines__()) + '\n'


# Viewport events
Viewport.register_event_type('on_enter')
Viewport.register_event_type('on_leave')
Viewport.register_event_type('on_resize')
Viewport.register_event_type('on_mouse_motion')
Viewport.register_event_type('on_mouse_drag')
Viewport.register_event_type('on_mouse_press')
Viewport.register_event_type('on_mouse_release')
Viewport.register_event_type('on_mouse_scroll')
Viewport.register_event_type('on_character')
Viewport.register_event_type('on_key_press')
Viewport.register_event_type('on_key_release')
Viewport.register_event_type('on_draw')

# Window events
#Viewport.register_event_type('on_init')
#Viewport.register_event_type('on_show')
#Viewport.register_event_type('on_hide')
#Viewport.register_event_type('on_close')
#Viewport.register_event_type('on_idle')
