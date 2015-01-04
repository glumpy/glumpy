#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app
from glumpy.graphics.collections import PointCollection
from glumpy.transforms import LogScale, Position3D, Viewport

window = app.Window(1024,1024, color=(1,1,1,1))

@window.event
def on_draw(dt):
    window.clear()
    points.draw()

transform = Position3D(LogScale()) + Viewport()
transform["domain"] = 1,2

points = PointCollection("agg", transform = transform)
P = np.random.uniform(1,10,(10000,3))
points.append(P*P)

app.run()
