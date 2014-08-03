#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
import glumpy as gp
import glumpy.gl as gl
from glumpy.graphics.collection import SolidSegmentCollection


window = gp.app.Window(width=1200, height=600)

@window.event
def on_draw(dt):
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    C.draw()

@window.event
def on_resize(width, height):
    gl.glViewport(0, 0, width, height)
    projection = gp.glm.ortho(0, width, 0, height, -1, +1)
    C['projection'] = projection


n = 100
P0 = np.ones((n,2))*50
P1 = np.ones((n,2))*550
P0[:,0] = np.linspace(100,1100,n)
P1[:,0] = np.linspace(110,1110,n)
LW = np.linspace(1, 8, n)

C = SolidSegmentCollection(linewidth='local')
C.append(P0, P1, linewidth = LW)
C['antialias'] = 1

C['model'] = np.eye(4, dtype=np.float32)
C['view'] = np.eye(4, dtype=np.float32)

gl.glClearColor(1.0, 1.0, 1.0, 1.0)
gl.glDisable(gl.GL_DEPTH_TEST)
gl.glEnable(gl.GL_BLEND)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA);

gp.app.run()
