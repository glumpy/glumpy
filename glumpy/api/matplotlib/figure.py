# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All rights reserved.
# Distributed under the terms of the new BSD License.
# -----------------------------------------------------------------------------
from glumpy import app, gloo, gl

class Figure(object):
    def __init__(self, figsize=(10,10), dpi=72, color=(1,1,1,1)):
        width = int(round(figsize[0] * dpi))
        height = int(round(figsize[1] * dpi))
        self.window = app.Window(width=width, height=height, color=color,
                                 title = "Figure (matplotlib API)")
        self.root = app.Viewport()

    def on_draw(self, dt):
        self.window.clear()

    def show(self):
        self.window.push_handlers(self.root)
        self.window.push_handlers(self)
        app.run()

    def add_axes(self, rect):
        axes = Axes(rect)
        self.root.add(axes)
        return axes


vertex = """
attribute vec2 position;
void main()
{
    gl_Position = <transform(vec4(position,0,1))>;
}
"""

fragment = """
uniform vec4 color;
void main()
{
    <clipping>;
    gl_FragColor = color;
}
"""

class Axes(app.Viewport):

    def __init__(self, rect, color=(1,0,0,1)):
        position = rect[0], rect[1]
        size = rect[2], rect[3]
        anchor = 0,0
        aspect = None
        app.Viewport.__init__(self,size, position, anchor, aspect)


        self.program = gloo.Program(vertex, fragment, count=4)
        self.program['position'] = [(-1,-1), (-1,+1), (+1,-1), (+1,+1)]
        self.program['color'] = color

        # WARNING: copy=false is mandatory here
        self.program["transform"] = self.transform(copy=False)
        self.program["clipping"] = self.clipping(copy=False)


    def on_draw(self, dt):
        self.program.draw(gl.GL_TRIANGLE_STRIP)
