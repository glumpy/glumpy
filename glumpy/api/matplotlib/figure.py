# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All rights reserved.
# Distributed under the terms of the new BSD License.
# -----------------------------------------------------------------------------
from glumpy import app, gloo, gl


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

    def add_axes(self, rect, facecolor=(1,1,1,1), aspect=None):
        axes = Axes(rect, facecolor, aspect)
        self.viewport.add(axes)
        return axes


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

    def __init__(self, rect, facecolor=(1,1,1,1), aspect=None):
        size = rect[2], rect[3]
        position = rect[0]+size[0]/2, rect[1]+size[1]/2
        anchor = 0.5, 0.5
        app.Viewport.__init__(self, size, position, anchor, aspect)
        self.program = gloo.Program(vertex, fragment, count=4)
        self.program['position'] = [(-1,-1), (-1,+1), (+1,-1), (+1,+1)]
        self.program['color'] = facecolor
        self.program['viewport'] = self.viewport


    def add_axes(self, rect, facecolor=(1,1,1,1), aspect=None):
        axes = Axes(rect, facecolor, aspect)
        self.add(axes)
        return axes

    def on_draw(self, dt):
        self.program.draw(gl.GL_TRIANGLE_STRIP)
        app.Viewport.on_draw(self,dt)
