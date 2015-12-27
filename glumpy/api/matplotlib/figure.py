# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
from glumpy import app, gloo, gl, transforms
from . axes import Axes

class Figure(object):
    """ """

    def __init__(self, figsize=(10,10), dpi=72, color=(.95,.95,.95,1)):
        width = int(round(figsize[0] * dpi))
        height = int(round(figsize[1] * dpi))
        self.window = app.Window(width=width, height=height, color=color,
                                 title = "Figure (matplotlib API)")
        self.viewport = app.Viewport()


    def on_draw(self, dt):
        self.window.clear()


    def show(self):
        self.window.push_handlers(self.viewport)
        self.window.push_handlers(self)
        app.run()


    def add_axes(self, rect=[0,0,1,1], facecolor=(1,1,1,1),
                 xscale = None, yscale = None, zscale = None,
                 projection = None, interface = None, aspect=None):
        axes = Axes(rect=rect, facecolor=facecolor, aspect=aspect,
                    xscale=xscale, yscale=yscale, zscale=zscale,
                    projection=projection, interface=interface)
        self.viewport.add(axes)
        return axes
