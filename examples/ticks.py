#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, glm
from glumpy.graphics.collection import AggSolidSegmentCollection
from glumpy.transforms import Position3D, Trackball, OrthographicProjection, PanZoom, Viewport

window = app.Window(width=1200, height=800, color=(1,1,1,1))

@window.event
def on_draw(dt):
    window.clear()
    collection.draw()

@window.event
def on_key_press(key, modifiers):
    if key == app.window.key.SPACE:
        transform.reset()

# Viewport is a transform that update a uniform (viewport) describing the
# current viewport. It is required for computing the line width.
# transform = PanZoom(OrthographicProjection(Position3D()), aspect=None) + Viewport()
transform = Trackball((Position3D())) + Viewport()
window.attach(transform)

collection = AggSolidSegmentCollection(transform=transform,
                                       linewidth='local', color='local')


# xmin,xmax = 0,800
# ymin,ymax = 0,800
xmin,xmax = -1,1
ymin,ymax = -1,1



# Frame
# -------------------------------------
P0 = [(xmin,ymin,0), (xmin,ymax,0), (xmax,ymax,0), (xmax,ymin,0)]
P1 = [(xmin,ymax,0), (xmax,ymax,0), (xmax,ymin,0), (xmin,ymin,0)]
collection.append(P0, P1, linewidth=2)

# Grids
# -------------------------------------
# n = 10
# P0 = np.zeros((n-2,3))
# P1 = np.zeros((n-2,3))

# P0[:,0] = np.linspace(xmin,xmax,n)[1:-1]
# P0[:,1] = ymin
# P1[:,0] = np.linspace(xmin,xmax,n)[1:-1]
# P1[:,1] = ymax
# collection.append(P0, P1, linewidth=1, color=(0,0,0,.25))

# P0 = np.zeros((n-2,3))
# P1 = np.zeros((n-2,3))
# P0[:,0] = xmin
# P0[:,1] = np.linspace(ymin,ymax,n)[1:-1]
# P1[:,0] = xmax
# P1[:,1] = np.linspace(ymin,ymax,n)[1:-1]
# collection.append(P0, P1, linewidth=1, color=(0,0,0,.25))


# Majors
# -------------------------------------
n = 10
P0 = np.zeros((n-2,3))
P1 = np.zeros((n-2,3))
P0[:,0] = np.linspace(xmin,xmax,n)[1:-1]
P0[:,1] = ymin
P1[:,0] = np.linspace(xmin,xmax,n)[1:-1]
P1[:,1] = ymin + 0.025 * (ymax-ymin)
collection.append(P0, P1, linewidth=1.5)
P0[:,1] = ymax
P1[:,1] = ymax - 0.025 * (ymax-ymin)
collection.append(P0, P1, linewidth=1.5)

P0 = np.zeros((n-2,3))
P1 = np.zeros((n-2,3))
P0[:,0] = xmin
P0[:,1] = np.linspace(ymin,ymax,n)[1:-1]
P1[:,0] = xmin + 0.025 * (xmax-xmin)
P1[:,1] = np.linspace(ymin,ymax,n)[1:-1]
collection.append(P0, P1, linewidth=1.5)
P0[:,0] = xmax
P1[:,0] = xmax - 0.025 * (xmax-xmin)
collection.append(P0, P1, linewidth=1.5)


# Minors
# -------------------------------------
n = 100
P0 = np.zeros((n-2,3))
P1 = np.zeros((n-2,3))
P0[:,0] = np.linspace(xmin,xmax,n)[1:-1]
P0[:,1] = ymin
P1[:,0] = np.linspace(xmin,xmax,n)[1:-1]
P1[:,1] = ymin + 0.0125 * (ymax-ymin)
collection.append(P0, P1, linewidth=1)
P0[:,1] = ymax
P1[:,1] = ymax - 0.0125 * (ymax-ymin)
collection.append(P0, P1, linewidth=1)

P0 = np.zeros((n-2,3))
P1 = np.zeros((n-2,3))
P0[:,0] = xmin
P0[:,1] = np.linspace(ymin,ymax,n)[1:-1]
P1[:,0] = xmin + 0.0125 * (xmax-xmin)
P1[:,1] = np.linspace(ymin,ymax,n)[1:-1]
collection.append(P0, P1, linewidth=1)
P0[:,0] = xmax
P1[:,0] = xmax - 0.0125 * (xmax-xmin)
collection.append(P0, P1, linewidth=1)



app.run()
