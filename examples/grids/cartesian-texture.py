#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
import glumpy.gl as gl
import glumpy.app as app
import glumpy.gloo as gloo

vertex   = "./grid-test.vert"
fragment = "./grid-test.frag"
window = app.Window(width=512, height=512)

@window.event
def on_draw():
    program.draw(gl.GL_TRIANGLE_STRIP)

@window.event
def on_resize(width, height):
    gl.glViewport(0, 0, width, height)

program = gloo.Program(vertex, fragment, 4)

program['a_position'] = (-1, -1), (-1, 1), (1, -1), (1, 1)
program['a_texcoord'] = (0, 0), (0, +1), (+1, 0), (+1, +1)
program['u_texture'] = np.linspace(0,1,16);
program['u_texture'].interpolation = gl.GL_LINEAR
program['u_texture'].wrapping = gl.GL_CLAMP_TO_EDGE

app.run()
