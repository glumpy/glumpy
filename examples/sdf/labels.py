#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import numpy as np
import glumpy as gp
import glumpy.gl as gl
import glumpy.glm as glm
from sdf_font import SDFFont


window = gp.Window(width=700, height=700)

@window.event
def on_draw():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    C.draw()

@window.event
def on_resize(width, height):
    gl.glViewport(0, 0, width, height)
    C['projection'] = glm.ortho(0, width, 0, height, -1, +1)
    i = 0
    for x in [0,width//2, width]:
        for y in [0,height//2, height]:
            C[i]['translate'] = x,y
            i += 1

@window.event
def on_mouse_scroll(x, y, dx, dy):
    scale = C["scale"][0]
    C["scale"] = min(max(0.01, scale + .01 * dy * scale), 100)



font = SDFFont("Vera.ttf")

C = gp.GlyphCollection(dtypes=[('translate', np.float32, 2)],
                       translate='shared')

for anchor_x in ['left', 'center', 'right']:
    for anchor_y in ['bottom', 'center', 'top']:
        C.append("Hello", font, anchor_x=anchor_x, anchor_y=anchor_y, color=(0,0,0,1))

theta,dtheta = 0,0
C['u_kernel'] = np.load("spatial-filters.npy")
C['atlas_data'] = font.atlas
C['atlas_data'].interpolation = gl.GL_LINEAR
C['atlas_shape'] = font.atlas.shape[1],font.atlas.shape[0]
C['scale'] = 1.0
C['model'] = np.eye(4, dtype=np.float32)


gl.glClearColor(1.0, 1.0, 1.0, 1.0)
gl.glDisable(gl.GL_DEPTH_TEST)
gl.glEnable(gl.GL_BLEND)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
gp.run()
