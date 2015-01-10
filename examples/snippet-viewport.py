#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gl, glm, gloo
from glumpy.transforms import Position


vertex = """
attribute vec2 position;
void main()
{
    gl_Position = <transform>;
    //gl_Position = vec4(position,0,1);
}
"""

fragment = """
void main()
{
    <clipping>;
    gl_FragColor = vec4(1,0,0,1);
}
"""

window = app.Window(width=800, height=800)

@window.event
def on_draw(dt):
    window.clear()
    program.draw(gl.GL_TRIANGLE_STRIP)

program = gloo.Program(vertex, fragment, count=4)
program['position'] = [(-1,-1), (-1,+1), (+1,-1), (+1,+1)]

# -- Child has size of root -10 pixels
child = app.Viewport(size=(-10,-10), position=(0.5,0.5), anchor=(0.5,0.5))

# -- Child has 95% of size of root
# child = app.Viewport(size=(.95,.95), position=(0.5,0.5), anchor=(0.5,0.5), aspect=1)

# -- Child has a (fixed) size of 256x256
# child = app.Viewport(size=(256,256), position=(0.5,0.5), anchor=(0.5,0.5), aspect=1)

# -- Child is at bottom-left corner
# child = app.Viewport(size=(256,256), position=(0.0,0.0), anchor=(0.0,0.0), aspect=1)

# -- Child is at top-right corner
# child = app.Viewport(size=(256,256), position=(-1,-1), anchor=(-1,-1), aspect=1)

# -- Child is at top-right corner
# child = app.Viewport(size=(0.5,0.5), position=(-1,-1), anchor=(-1,-1), aspect=1)

viewport = app.Viewport()
window.attach(viewport)
viewport.add(child)

program["transform"] = child.transform(Position("position"))
program["clipping"] = child.clipping(copy=False)

app.run()
