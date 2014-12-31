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


figure = matplotlib.Figure((16,8))
left  = figure.add_axes([0.010, 0.01, 0.485, 0.98], facecolor=(1,0,0,0.25), aspect=1)
_right = left.add_axes([0.505, 0.01, 0.485, 0.98], facecolor=(0,0,1,0.25), aspect=1)
right = _right.add_axes([0.505, 0.01, 0.485, 0.48], facecolor=(0,0,1,0.25), aspect=1)

trackball = Trackball(Position3D())
left.attach(trackball)
collection = PointCollection("agg", transform=trackball)

panzoom = PanZoom(OrthographicProjection(Position3D(), normalize=True))
right.attach(panzoom)
view = collection.view(transform=panzoom)

collection.append(np.random.normal(0,.5,(100,3)))

@left.event
def on_draw(dt):
    collection.draw()

@right.event
def on_draw(dt):
    view.draw(gl.GL_POINTS)

figure.show()
