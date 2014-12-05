#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, glm
from glumpy.graphics.collection import AggSolidSegmentCollection
from glumpy.transforms import Position2D, OrthographicProjection, PanZoom, Viewport

window = app.Window(width=1200, height=600, color=(1,1,1,1))

@window.event
def on_draw(dt):
    window.clear()
    collection.draw()

n = 100
P0 = np.ones((n,2))*50
P1 = np.ones((n,2))*550
P0[:,0] = np.linspace(100,1100,n)
P1[:,0] = np.linspace(110,1110,n)


transform = OrthographicProjection(Position2D("position")) + Viewport()
window.attach(transform)

collection = AggSolidSegmentCollection(linewidth='local', transform=transform)
collection.append(P0, P1, linewidth = np.linspace(1, 8, n))
collection['antialias'] = 1

app.run()
