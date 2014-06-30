#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import numpy as np

import glumpy
import glumpy.gl as gl
import glumpy.app as app
import glumpy.gloo as gloo


vertex = """
attribute vec2 a_position;
void main() {
    gl_Position = vec4(a_position, 0.0, 1.0);
    gl_PointSize = 30.0;
}
"""

fragment1 = """
void main() {
    gl_FragColor = vec4(0.0, 0.0, 1.0, 1.0);
}
"""

fragment2 = """
void main() {
    gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
}
"""


program1 = gloo.Program(vertex, fragment1)  # blue on the left
program1['a_position'] = np.zeros((1,2),dtype=np.float32) + 0.5
program2 = gloo.Program(vertex, fragment2)  # red on the right
program2['a_position'] = np.zeros((1,2),dtype=np.float32) - 0.5


window = app.Window()
@window.event
def on_draw():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    program1.draw(gl.GL_POINTS)
    program2.draw(gl.GL_POINTS)

@window.event
def on_resize(width,height):
    gl.glViewport(0, 0, width, height)

gl.glDisable(gl.GL_DEPTH_TEST)
gl.glEnable(gl.GL_VERTEX_PROGRAM_POINT_SIZE)
gl.glEnable(gl.GL_POINT_SPRITE)

app.run()
