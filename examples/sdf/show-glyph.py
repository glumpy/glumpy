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

from font import Font


window = app.Window(width=800, height=800)

@window.event
def on_draw():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    program.draw(gl.GL_TRIANGLE_STRIP)

@window.event
def on_resize(width, height):
    gl.glViewport(0, 0, width, height)

@window.event
def on_mouse_scroll(x, y, dx, dy):
    scale = program["scale"][0]
    program["scale"] = min(max(0.01, scale + .01 * dy * scale), 1)

program = gloo.Program("sdf.vert", ["spatial-filters.frag", "sdf-2.frag"], count=4)
program['position'] = [(-1,-1), (-1,+1), (+1,-1), (+1,+1)]



font = Font("Vera.ttf")
glyph_a = font["W"]
u0,v0,u1,v1 = glyph_a.texcoords
#program['texcoord'] = [( 0, 1), ( 0, 0), ( 1, 1), ( 1, 0)]
program['texcoord'] = [(u0,v1), (u0,v0), (u1,v1), (u1,v0)]
program['u_kernel'] = np.load("spatial-filters.npy")
program['tex_data'] = font.atlas
program['tex_data'].interpolation = gl.GL_LINEAR
program['tex_shape'] = font.atlas.shape[1],font.atlas.shape[0]
program['color'] = 0,0,0,1
program['scale'] = 1.0

gl.glClearColor(1.0, 1.0, 1.0, 1.0)
gl.glDisable(gl.GL_DEPTH_TEST)
gl.glEnable(gl.GL_BLEND)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

app.run()
