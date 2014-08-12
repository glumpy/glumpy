#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
""" This example shows standard orthographic projection transform. """

import numpy as np
from  glumpy import app, gl, glm, gloo
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

window = app.Window(width=800, height=800)

@window.event
def on_draw(dt):
    window.clear()
    program.draw(gl.GL_TRIANGLE_STRIP)

@window.event
def on_resize(w, h):
    program['position'] = [(w-100,h-100), (w-100,h), (w,h-100), (w,h)]

transform = OrthographicProjection(Position2D("position"))
program = gloo.Program(vertex, fragment, count=4)
program["transform"] = transform
window.attach(transform)
app.run()
