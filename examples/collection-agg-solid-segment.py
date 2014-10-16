#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, glm
from glumpy.graphics.collection import AggSolidSegmentCollection


window = app.Window(width=1200, height=600, color=(1,1,1,1))

@window.event
def on_draw(dt):
    window.clear()
    C.draw()

@window.event
def on_resize(width, height):
    C['projection'] = glm.ortho(0, width, 0, height, -1, +1)

n = 100
P0 = np.ones((n,2))*50
P1 = np.ones((n,2))*550
P0[:,0] = np.linspace(100,1100,n)
P1[:,0] = np.linspace(110,1110,n)
LW = np.linspace(1, 8, n)

C = AggSolidSegmentCollection(linewidth='local')
C.append(P0, P1, linewidth = LW)
C['antialias'] = 1
C['model'] = np.eye(4, dtype=np.float32)
C['view'] = np.eye(4, dtype=np.float32)

app.run()
