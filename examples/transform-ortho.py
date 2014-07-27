#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import numpy as np
import glumpy as gp
import glumpy.gl as gl
from glumpy.transforms import OrthographicProjection, Position2D


vertex = """
attribute vec2 position;
void main()
{
    gl_Position = <transform>;
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

transform = gp.transforms.OrthographicProjection(Position2D("position"))
program = gp.gloo.Program(vertex, fragment, count=4)
program["transform"] = transform
window.attach(transform)
gp.run()
