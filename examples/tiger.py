#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import re
import triangle
import numpy as np
import xml.dom
import xml.dom.minidom

from glumpy import app, gl
from glumpy.graphics.svg import Style, Path
from glumpy.graphics.collection import PathCollection
from glumpy.graphics.collection import TriangleCollection
from glumpy.transforms import Position3D, OrthographicProjection, PanZoom, Viewport



window = app.Window(1000, 1000, color=(1,1,1,1))
transform = PanZoom(OrthographicProjection(Position3D())) + Viewport()
window.attach(transform)


@window.event
def on_draw(dt):
    window.clear()
    triangles.draw()
    paths.draw()

@window.event
def on_init():
    gl.glEnable(gl.GL_DEPTH_TEST)

@window.event
def on_key_press(key, modifiers):
    if key == app.window.key.SPACE:
        transform.reset()


triangles = TriangleCollection("agg", transform=transform)
paths = PathCollection("agg+", transform=transform, linewidth='shared')
paths["miter_limit"] = 4.0
paths["linewidth"] = 1.0


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
    paths = []
    for tag in tag.getElementsByTagName('g'):
        style = Style(tag.getAttribute("style"))
        for item in tag.getElementsByTagName('path'):
            path = Path(item.getAttribute('d'))
            paths.append( (path, style) )
    return paths

def length((x0,y0), (x1,y1)):
    dx,dy = (x1-x0), (y1-y0)
    return dx*dx+dy*dy

z = 500
for path, style in svg_open("tiger.svg"):
    for V in path.vertices:
        if len(V) < 3: continue
        closed = False
        if length(V[0], V[-1]) == 0:
            closed = True
            V = V[:-1]
        P = np.zeros((len(V),3))
        P[:,:2] = V
        P *= (2,-2,1)
        P += (350,700,0)
        if style.stroke is not None:
            P[:,2] = z-1
            paths.append(P, closed=closed, color=style.stroke.rgba,
                         linewidth = style.stroke_width)

        if style.fill is not None:
            P,I = triangulate(P)
            P[:,2] = z
            triangles.append(P, I, color=style.fill.rgba)
        z -= 1

app.run()
