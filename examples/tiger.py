#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import re
import triangle
import numpy as np

from glumpy import app, gl, data
from glumpy.graphics.svg import Document
from glumpy.graphics.collections import PathCollection, TriangleCollection
from glumpy.transforms import Position3D, OrthographicProjection, PanZoom, Viewport


tiger = Document(data.get("tiger.svg"))
window = app.Window(int(tiger.viewport.width),
                    int(tiger.viewport.height),
                    color=(1,1,1,1))
transform = PanZoom(OrthographicProjection(Position3D(), yinvert=True)) + Viewport()
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



z = 0
for path in tiger.paths:
    for vertices,closed in path.vertices:
        if len(vertices) < 3:
            continue
        if path.style.stroke is not None:
            vertices[:,2] = z+0.5
            paths.append(vertices, closed=closed, color=path.style.stroke.rgba,
                         linewidth = path.style.stroke_width or 0.1)
        if path.style.fill is not None:
             V,I = triangulate(vertices)
             V[:,2] = z
             triangles.append(V, I, color=path.style.fill.rgba)
    z += 1

app.run()
