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
from glumpy.transforms import Position, Trackball, OrthographicProjection, PanZoom, Viewport


figure = matplotlib.Figure((16,8))
left  = figure.add_axes([0.010, 0.01, 0.485, 0.98], facecolor=(1,0,0,0.25), aspect=1)
right = figure.add_axes([0.505, 0.01, 0.485, 0.98], facecolor=(0,0,1,0.25), aspect=1)

trackball = Trackball(Position(), aspect=1.0)
collection = PointCollection("agg", transform=trackball, viewport=left.viewport)

panzoom = PanZoom(OrthographicProjection(Position(), normalize=True))
view = collection.view(transform=panzoom, viewport=right.viewport)

collection.append(np.random.normal(0,.5,(5000,3)))

@left.event
def on_draw(dt):
    collection.draw()

@right.event
def on_draw(dt):
    view.draw(gl.GL_POINTS)


left.attach(collection["transform"])
right.attach(view["transform"])
figure.show()
