#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, glm, gl
from glumpy.graphics.collection import PathCollection
from glumpy.transforms import Position3D, Viewport, OrthographicProjection, PanZoom


window = app.Window(width=800, height=800, color=(1,1,1,1))

def star(inner=0.5, outer=1.0, n=5):
    R = np.array( [inner,outer]*n)
    T = np.linspace(0,2*np.pi,2*n,endpoint=False)
    P = np.zeros((2*n,3))
    P[:,0]= R*np.cos(T)
    P[:,1]= R*np.sin(T)
    return P

def spiral(n = 1024):
    T = np.linspace(0, 10*2*np.pi, n)
    R = np.linspace(10, 400, n)
    P = np.zeros((n,3), dtype=np.float32)
    P[:,0] = 400 + np.cos(T)*R
    P[:,1] = 400 + np.sin(T)*R
    return P

@window.event
def on_draw(dt):
    window.clear()
    paths.draw()

@window.event
def on_key_press(key, modifiers):
    if key == app.window.key.SPACE:
        transform.reset()

# Viewport is a transform that update a uniform (viewport) describing the
# current viewport. It is required for computing the line width.
transform = PanZoom(OrthographicProjection(Position3D()), aspect=None) + Viewport()
window.attach(transform)

paths = PathCollection(mode="agg", transform=transform)
x,y, scale = 400, 400, 300
paths.append(star(n=25)*scale + (x,y,0), closed=True)

paths["linewidth"] = 10.0
app.run()
