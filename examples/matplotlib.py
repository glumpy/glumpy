#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy.api import matplotlib
from glumpy import gl, library
from glumpy.graphics.collections import PointCollection, Collection
from glumpy.transforms import Position3D, Trackball, OrthographicProjection, PanZoom


figure = matplotlib.Figure((12,6))
left  = figure.add_axes([0.010, 0.01, 0.485, 0.98], facecolor=(1,0,0,0.25), aspect=1)
right = figure.add_axes([0.505, 0.01, 0.485, 0.98], facecolor=(0,0,1,0.25), aspect=1)

panzoom = PanZoom(OrthographicProjection(Position3D(), aspect=None, normalize=True))
left.attach(panzoom)
collection = PointCollection("agg", transform=panzoom)
view = C_left

# trackball = Trackball(Position3D())
# right.attach(trackball)
# C = Collection("agg", transform=panzoom)
# C = PointCollection("agg")

print C_


C_left.append(np.random.normal(0,.5,(1000,3)))

@left.event
def on_draw(dt):
    collection.draw()

@right.event
def on_draw(dt):
    view.draw()

figure.show()
