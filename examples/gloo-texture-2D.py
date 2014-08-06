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
    attribute vec2 position;
    attribute vec2 texcoord;
    varying vec2 v_texcoord;
    void main()
    {
        gl_Position = vec4(position, 0.0, 1.0);
        v_texcoord = texcoord;
    }
"""

fragment = """
    uniform sampler2D texture;
    varying vec2 v_texcoord;
    void main()
    {
        gl_FragColor = texture2D(texture, v_texcoord);
    }
"""

def checkerboard(grid_num=8, grid_size=32):
    row_even = grid_num / 2 * [0, 1]
    row_odd = grid_num / 2 * [1, 0]
    Z = np.row_stack(grid_num / 2 * (row_even, row_odd)).astype(np.uint8)
    return 255 * Z.repeat(grid_size, axis=0).repeat(grid_size, axis=1)

window = app.Window(width=800, height=800)

@window.event
def on_draw(dt):
    program.draw(gl.GL_TRIANGLE_STRIP)

@window.event
def on_resize(width, height):
    gl.glViewport(0, 0, width, height)

program = gloo.Program(vertex, fragment, count=4)
program['position'] = [(-1,-1), (-1,+1), (+1,-1), (+1,+1)]
program['texcoord'] = [( 0, 1), ( 0, 0), ( 1, 1), ( 1, 0)]
program['texture'] = checkerboard()
app.run()
