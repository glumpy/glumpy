#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, glm
from glumpy.graphics.collection import SegmentCollection
from glumpy.transforms import Position3D, OrthographicProjection, PanZoom, Viewport

window = app.Window(width=1200, height=600, color=(1,1,1,1))

@window.event
def on_draw(dt):
    window.clear()
    collection.draw()

@window.event
def on_key_press(key, modifiers):
    if key == app.window.key.SPACE:
        transform.reset()

n = 100
P0 = np.dstack((np.linspace(100,1100,n),np.ones(n)* 50,np.zeros(n))).reshape(n,3)
P1 = np.dstack((np.linspace(110,1110,n),np.ones(n)*550,np.zeros(n))).reshape(n,3)

# Viewport is a transform that update a uniform (viewport) describing the
# current viewport. It is required for computing the line width.
transform = PanZoom(OrthographicProjection(Position3D()), aspect=None) + Viewport()
window.attach(transform)

collection = SegmentCollection(mode="agg", linewidth='local', transform=transform)
collection.append(P0, P1, linewidth = np.linspace(1, 8, n))
collection['antialias'] = 1

#collection = SegmentCollection(mode="raw", transform=transform)
#collection.append(P0, P1)

app.run()
