#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app
from glumpy.transforms import Position3D, Viewport
from glumpy.graphics.collections import PointCollection


window = app.Window(1024,1024, color=(1,1,1,1))

points = PointCollection("agg", color="shared")
points.append(np.random.normal(0.0,0.5,(100000,3)), itemsize=50000)
points["color"] = (1,0,0,1), (0,0,1,1)

#points["viewport"].transform = True
#points["viewport"].clipping = True
#points["viewport"].viewport = 256,256,512,512


@window.event
def on_draw(dt):
    window.clear()
    points.draw()

window.attach(points["transform"])
window.attach(points["viewport"])
app.run()
