#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, glm, gl, library
from glumpy.transforms import *
from glumpy.graphics.collections import *
from glumpy.graphics.text import FontManager


def linepath(P0, P1, n=100):
    P = np.zeros((n,3))
    xmin,ymin,zmin = P0
    xmax,ymax,zmax = P1
    P[:,0] = np.linspace(xmin, xmax, n, endpoint=True)
    P[:,1] = np.linspace(ymin, ymax, n, endpoint=True)
    P[:,2] = np.linspace(zmin, zmax, n, endpoint=True)
    return P

window = app.Window(width=1200, height=1200, color=(1,1,1,1))

@window.event
def on_draw(dt):
    window.clear()
    labels.draw()
    ticks.draw()
    paths.draw()

xscale = LinearScale(".x", name="xscale", domain=[0,1], range=[0.25,1])
yscale = LinearScale(".y", name="yscale", domain=[0,1], range=[0,2*np.pi])
zscale = LinearScale(".z", name="zscale")
transform = Trackball(PolarProjection(Position(xscale,yscale,zscale)), aspect=1)
viewport = Viewport()

xmin,xmax = 0,1
ymin,ymax = 0,1
zmin,zmax = 0,1


# Outer Frame
# -------------------------------------
paths = PathCollection("agg", linewidth="shared", color="shared",
                       transform=transform, viewport=viewport)

paths.append(linepath((xmin,ymin,zmin),(xmax,ymin,zmin)), linewidth=2.0)
paths.append(linepath((xmin,ymax,zmin),(xmax,ymax,zmin)), linewidth=2.0)

paths.append(linepath((xmax,ymin,zmin),(xmax,ymax,zmin)), linewidth=2.0)
paths.append(linepath((xmin,ymin,zmin),(xmin,ymax,zmin)), linewidth=2.0)

paths.append(linepath((xmin,ymin,zmin),(xmin,ymin,zmax)), linewidth=2.0)

# Grids
# -------------------------------------
n = 10+1
X = np.linspace(xmin,xmax,n)[1:-1]
for x in X:
    paths.append(linepath((x,ymin,zmin),(x,ymax,zmin)),
                 linewidth=1.0, color=(0,0,0,.25))
Y = np.linspace(ymin,ymax,n)[1:-1]
for y in Y:
    paths.append(linepath((xmin,y,zmin),(xmax,y,zmin)),
                 linewidth=1.0, color=(0,0,0,.25))

# Ticks
# -------------------------------------
ticks = SegmentCollection("agg", transform=transform, viewport=viewport)

n_major = 10+1
n_minor = 50+1
length_major = 0.02
length_minor = 0.01

for x in np.linspace(xmin,xmax,n_major)[0:-1]:
    paths.append(linepath((x,ymin,zmin),(x,ymin+length_major,zmin)),
                 linewidth=2.0, color=(0,0,0,1))
for x in np.linspace(xmin,xmax,n_minor)[0:-1]:
    paths.append(linepath((x,ymin,zmin),(x,ymin+length_minor,zmin)),
                 linewidth=1.0, color=(0,0,0,1))

length_major = 0.04
length_minor = 0.02
for y in np.linspace(ymin,ymax,n_major)[0:-1]:
    paths.append(linepath((xmax,y,zmin),(xmax-length_major,y,zmin)),
                 linewidth=2.0, color=(0,0,0,1))
for y in np.linspace(ymin,ymax,n_minor)[0:-1]:
    paths.append(linepath((xmax,y,zmin),(xmax-length_minor,y,zmin)),
                 linewidth=1.0, color=(0,0,0,1))

for z in np.linspace(zmin,zmax,n_major)[0:-1]:
    paths.append(linepath((xmin,ymin,z),(xmin+length_major,ymin,z)),
                 linewidth=2.0, color=(0,0,0,1))
for z in np.linspace(zmin,zmax,n_minor)[0:-1]:
    paths.append(linepath((xmin,ymin,z),(xmin+length_minor,ymin,z)),
                 linewidth=1.0, color=(0,0,0,1))

# Tick labels
# -------------------------------------
labels = GlyphCollection(transform=transform, viewport=viewport,
                         vertex = 'collections/sdf-glyph-ticks.vert')


regular = FontManager.get("OpenSans-Regular.ttf")
n = 10+1
scale = 0.0075
for i,y in enumerate(np.linspace(xmin,xmax,n)[:-1]):
    text = "%.2f" % (i/10.0)
    labels.append(text, regular,
                  origin = (xmax+0.15,y,zmin), scale = scale, direction = (1,0,0),
                  anchor_x = "left", anchor_y = "center")
    labels.append(text, regular, origin = (y, -.001, zmin),
                  scale= scale, direction = (0,1,0),
                  anchor_x = "right", anchor_y = "center")


# Add some points
n = 1000
P = np.zeros((n,3))
P[:,0] = np.linspace(+1,0,n)
P[:,1] = np.linspace(0,5,n)
P[:,2] = np.linspace(-1,1,n)
paths.append(P, linewidth=3, color=(1,0,0,1))

window.attach(paths["transform"])
window.attach(paths["viewport"])

# time = 0
# @window.timer(1/60.0)
# def timer(elapsed):
#     global time
#     time += elapsed
#     paths["transform"]["yscale"]["range"] = 0, np.pi * (1.5 + 0.5*np.cos(time))

app.run()
