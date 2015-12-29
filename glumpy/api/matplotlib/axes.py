# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gloo, gl, transforms
from glumpy.graphics.collections import PointCollection


vertex = """
attribute vec2 position;
void main()
{
    gl_Position = vec4(position,0,1);
    <viewport.transform>;
}
"""

fragment = """
uniform vec4 color;
void main()
{
    gl_FragColor = color;
    <viewport.clipping>;
}
"""

class Axes(app.Viewport):
    """ """

    def __init__(self, rect=[0,0,1,1], facecolor=(1,1,1,1),
                 xscale = None, yscale = None, zscale = None,
                 projection = None, interface = None, aspect=None):

        size = rect[2], rect[3]
        position = rect[0]+size[0]/2, rect[1]+size[1]/2
        anchor = 0.5, 0.5
        app.Viewport.__init__(self, size, position, anchor, aspect)
        xscale = xscale if xscale is not None else transforms.LinearScale()
        yscale = yscale if yscale is not None else transforms.LinearScale()
        zscale = zscale if zscale is not None else transforms.LinearScale()
        projection = projection if projection is not None else transforms.IdentityProjection()
        interface = interface if interface is not None else transforms.Position()

        self._viewport = transforms.Viewport()
        xscale = xscale('.x', name = 'xscale')
        yscale = yscale('.y', name = 'yscale')
        zscale = zscale('.z', name = 'zscale')

        self._scale = transforms.Position(xscale, yscale, zscale)
        self._projection = projection #transforms.IdentityProjection()
        self._interface = interface(aspect=aspect)

        self.program = gloo.Program(vertex, fragment, count=4)
        self.program['position'] = [(-1,-1), (-1,+1), (+1,-1), (+1,+1)]
        self.program['color'] = facecolor
        self.program['viewport'] = self._viewport

        self._transform = self._interface(self._projection(self._scale))
        self.attach(self._transform)
        self._drawables = []


    def add_drawable(self, collection):
        drawable = collection.view(transform=self._transform, viewport= self._viewport)
        self._drawables.append(drawable)


    @property
    def viewport(self):
        """ Viewport transform  """

        return self._viewport

    @property
    def transform(self):
        """ Global transform """

        return self._transform

    @property
    def scale(self):
        """ Scale transform """

        return self._scale


    def add_axes(self, rect=[0,0,1,1], facecolor=(1,1,1,1),
                 xscale = None, yscale = None, zscale = None,
                 projection = None, interface = None, aspect=None):
        axes = Axes(rect=rect,facecolor=facecolor, aspect=aspect,
                    xscale=xscale, yscale=yscale, zscale=zscale,
                    projection=projection, interface=interface)
        self.add(axes)
        return axes


    def on_draw(self, dt):
        self.program.draw(gl.GL_TRIANGLE_STRIP)
        for drawable in self._drawables:
            drawable.draw()
        app.Viewport.on_draw(self,dt)


    def on_resize(self, width, height):
        if self.parent == None:
            self._requested_size = width, height
        self._compute_viewport()
        self.dispatcher.dispatch_event("on_resize", self.size[0], self.size[1])

        if self.viewport.is_attached:
            # self._viewport.dispatch_event("on_resize", width, height)
            self._viewport["global"]  = self.root.extents
            self._viewport["extents"] = self.extents

        for child in self._children:
            child.dispatch_event("on_resize", width, height)
