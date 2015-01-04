#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app
from glumpy.graphics.collections import PointCollection
from glumpy.transforms import LinearScale, LogScale, Position3D, Viewport

window = app.Window(1024,1024, color=(1,1,1,1))

@window.event
def on_draw(dt):
    window.clear()
    points.draw()

# lin-lin
# x_transform = LinearScale("position.x", domain=(0,10))
# y_transform = LinearScale("position.y", domain=(0,10))

# log-lin
x_transform = LogScale("position.x",    domain=(-1,3))
y_transform = LinearScale("position.y", domain=(0,10))

# lin-log
# x_transform = LinearScale("position.x", domain=(0,10))
# y_transform = LogScale("position.y",    domain=(-1,3))

# log-log
# x_transform = LogScale("position.x",    domain=(-1,3))
# y_transform = LogScale("position.y",    domain=(-1,3))

z_transform = "position.z"
transform = Position3D(x_transform, y_transform, z_transform) + Viewport()
points = PointCollection("agg", transform = transform, color='local')

X = np.linspace(0.1,100.0,10000).reshape(10000,1)
Z = np.zeros((len(X),1))
points.append(np.hstack((X,         X, Z)), color=(1,0,0,1))
points.append(np.hstack((X, np.log(X), Z)), color=(0,1,0,1))
points.append(np.hstack((X,     10**X, Z)), color=(0,0,1,1))

app.run()
