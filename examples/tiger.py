#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------

import numpy as np

import re
import xml.dom
import xml.dom.minidom

#from pyhull.delaunay import DelaunayTri
#from pyhull.convex_hull import ConvexHull
# from scipy.spatial import Delaunay
import triangle

from glumpy import app, gl
from glumpy.geometry.path import Path
from glumpy.graphics.collection import PathCollection
from glumpy.graphics.collection import PointCollection
from glumpy.graphics.collection import SegmentCollection
from glumpy.graphics.collection import TriangleCollection
from glumpy.transforms import Position3D, OrthographicProjection, PanZoom, Viewport


def triangulate(P):
    P = np.array(P)
    z = P[0,2]

    n = len(P)
    P = P[:,:2]
    S = np.repeat(np.arange(n+1),2)[1:-1]
    S[-2:] = n-1,0
    T = triangle.triangulate({'vertices': P, 'segments': S}, "p")
    V2 = T["vertices"]
    I = T["triangles"]
    V3 = np.empty((len(V2),3))
    V3[:,:2] = V2
    V3[:,2] = z
    return V3, I



def svg_open(filename):
    dom = xml.dom.minidom.parse(filename)
    tag = dom.documentElement
    if tag.tagName != 'svg':
        raise ValueError('document is <%s> instead of <svg>'%tag.tagName)
    path_re = re.compile(r'([MLHVCSQTAZ])([^MLHVCSQTAZ]+)', re.IGNORECASE)
    float_re = re.compile(r'(?:[\s,]*)([+-]?\d+(?:\.\d+)?)')
    # path = Path()
    paths = []
    for tag in tag.getElementsByTagName('g'):

        style = tag.getAttribute("style")
        fill,stroke = None, None
        m = re.search("fill:\s*#(?P<value>[0-9a-fA-F]+)", style)
        if m:
            value = m.group("value")
            fill = np.array(tuple(ord(c) for c in value.decode('hex')))/256.0
        m = re.search("stroke\s*:\s*#(?P<value>[0-9a-fA-F]+)", style)
        if m:
            value = m.group("value")
            stroke = np.array(tuple(ord(c) for c in value.decode('hex')))/256.0

        for tag in tag.getElementsByTagName('path'):
            path = Path()
            for cmd, values in path_re.findall(tag.getAttribute('d')):
                points = [float(v) for v in float_re.findall(values)]
                path.svg_parse(cmd, points)
            paths.append( (path.vertices[0], stroke, fill) )

    return paths

# n = 1000
# P = np.random.normal(0,.25, (n,3))
# P[:,2] = 0
# I = np.array(ConvexHull(P[:,:2]).vertices)
# P0, P1 = P[I[:,0]], P[I[:,1]]
# T = np.array(DelaunayTri(P[:,:2]).vertices)

window = app.Window(800, 800, color=(1,1,1,1))
transform = PanZoom(OrthographicProjection(Position3D())) + Viewport()
#transform = Position3D() + Viewport()
window.attach(transform)


@window.event
def on_draw(dt):
    window.clear()
    triangles.draw()
    paths.draw()

@window.event
def on_init():
    gl.glEnable(gl.GL_DEPTH_TEST)



triangles = TriangleCollection("agg", transform=transform)
paths = PathCollection("agg+", transform=transform)
paths["miter_limit"] = 4.0
paths["linewidth"] = 1.0


def dist(v0,v1):
    x0,y0 = v0
    x1,y1 = v1
    dx,dy = (x1-x0), (y1-y0)
    return dx*dx+dy*dy

z = 500
for V, stroke, fill in svg_open("tiger.svg"):
    if len(V) < 3:
        continue
    closed = False
    if dist(V[0], V[-1]) == 0:
        closed = True
        V = V[:-1]
    P = np.zeros((len(V),3))
    P[:,:2] = V
    P *= (1,-1,1)

    if stroke is not None:
        P[:,2] = z-1
        paths.append(P, closed=closed, color=(stroke[0],stroke[1],stroke[2],1))
    if fill is not None:
        P,I = triangulate(P)
        P[:,2] = z
        triangles.append(P, I, color=(fill[0],fill[1],fill[2],1))
    z -= 1

app.run()
