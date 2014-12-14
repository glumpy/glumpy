#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, glm, gl
from glumpy.graphics.collection import AggSolidPathCollection
from glumpy.transforms import (Position3D, Viewport,
                               OrthographicProjection, Trackball, PanZoom)


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

def lorenz(n=100000):
    def iterate(P, s=10, r=28, b=2.667, dt=0.01):
        x, y, z = P
        x_dot = s*(y - x)
        y_dot = r*x - y - x*z
        z_dot = x*y - b*z
        return dt*x_dot, dt*y_dot, dt*z_dot

    # Need one more for the initial values
    P = np.empty((n+1,3))

    # Setting initial values
    P[0] = 0., 1., 1.05

    # Stepping through "time"
    dt = 100.0/n
    for i in range(n) :
        # Derivatives of the X, Y, Z state
        P[i+1] = P[i] + iterate(P[i], dt=dt)

    # Normalize
    vmin,vmax = P.min(),P.max()
    P = 2*(P-vmin)/(vmax-vmin) - 1

    # Centering
    P[:,0] -= (P[:,0].max() + P[:,0].min())/2.0
    P[:,1] -= (P[:,1].max() + P[:,1].min())/2.0
    P[:,2] -= (P[:,2].max() + P[:,2].min())/2.0

    return P

@window.event
def on_draw(dt):
    window.clear()
    # gl.glPolygonMode( gl.GL_FRONT_AND_BACK, gl.GL_LINE )
    paths.draw()

@window.event
def on_key_press(key, modifiers):
    if key == app.window.key.SPACE:
        transform.reset()

# Viewport is a transform that update a uniform (viewport) describing the
# current viewport. It is required for computing the line width.
# transform = PanZoom(OrthographicProjection(Position3D()), aspect=None) + Viewport()
transform = Trackball(Position3D()) + Viewport()
window.attach(transform)

paths = AggSolidPathCollection(transform=transform)
# paths.append(star(n=5)*350 + (400,400,0), closed=True)
# paths.append(spiral())
paths.append(lorenz())
paths["linewidth"] = 1.0
app.run()
