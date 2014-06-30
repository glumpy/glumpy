#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import numpy as np
import glumpy as gp
import glumpy.gl as gl

vertex = """
attribute vec2 position;
void main()
{
    gl_Position = transform(vec4(position, 0.0, 1.0));
}
"""

fragment = """
void main()
{
    gl_FragColor = vec4(1,0,0,1);
}
"""

window = gp.Window(width=800, height=800)

@window.event
def on_draw():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    program.draw(gl.GL_TRIANGLE_STRIP)

@window.event
def on_resize(w, h):
    program['position'] = [(w-100,h-100), (w-100,h), (w,h-100), (w,h)]

# This transform is aware of resize events
transform = gp.transforms.OrthographicProjection()

program = gp.gloo.Program(transform.code + vertex, fragment, count=4)

# We attach the program to the transform
transform.program = program

# We attach the transform to the window
window.push_handlers(transform)

app.run()
