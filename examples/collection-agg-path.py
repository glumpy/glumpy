#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All rights reserved.
# Distributed under the terms of the new BSD License.
# -----------------------------------------------------------------------------
# This implements antialiased lines using a geometry shader with correct joins
# and caps.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gl, glm, gloo
from glumpy.graphics.collection import AggPathCollection


# Nice spiral
def spiral(size=512, n=1024):
    T = np.linspace(0, 10*2*np.pi, n)
    R = np.linspace(10, size/2.0, n)
    P = np.zeros((n,2), dtype=np.float32)
    P[:,0] = size/2.0 + np.cos(T)*R
    P[:,1] = size/2.0 + np.sin(T)*R
    return P

# Star
def star(inner=0.45, outer=1.0, n=5):
    R = np.array( [inner,outer]*n)
    T = np.linspace(0,2*np.pi,2*n,endpoint=False)
    P = np.zeros((2*n,2))
    P[:,0]= R*np.cos(T)
    P[:,1]= R*np.sin(T)
    return P

window = app.Window(width=512, height=512, color=(1,1,1,1))
C = AggPathCollection()
#C.append(spiral(), linewidth=2.0)

# P = np.array([[100,600],
#               [400,600],
#               [700,600]], dtype=np.float32)
# C.append(P, linewidth=10.0)
# P = np.array([[100,200],
#               [400,200],
#               [700,200]], dtype=np.float32)
# C.append(P, linewidth=10.0)

#S = star(n=5)*12
#print len(s), s.shape
#P = np.zeros( (5000,len(s),2))
#P[:,...] = s
#P[:] += np.randim.uniform(0,512,(
#C.append(P, linewidth=2.0, itemsize=len(s), closed=True)

S = star(n=5)
for i in range(500):
    x,y = np.random.uniform(0,512,2)
    P = (S*12 + (x,y)).astype(np.float32)
    C.append(P, linewidth=3.0, closed=True)

@window.event
def on_draw(dt):
    window.clear()
    C.draw()

@window.event
def on_resize(width, height):
    C['projection'] = glm.ortho(0, width, 0, height, -1, +1)

app.run()
