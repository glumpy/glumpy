# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import re
import triangle
import numpy as np

from glumpy import app, gl, data
from glumpy.graphics.svg import Document
from glumpy.graphics.collections import PathCollection, PolygonCollection
from glumpy.transforms import Position, OrthographicProjection, PanZoom, Viewport


tiger = Document(data.get("tiger.svg"))
window = app.Window(int(tiger.viewport.width),
                    int(tiger.viewport.height),
                    color=(1,1,1,1))

@window.event
def on_draw(dt):
    window.clear()
    polygons.draw()
    paths.draw()

@window.event
def on_init():
    gl.glEnable(gl.GL_DEPTH_TEST)

@window.event
def on_key_press(key, modifiers):
    if key == app.window.key.SPACE:
        transform.reset()


transform = PanZoom(OrthographicProjection(Position(), yinvert=True), aspect=None)
paths = PathCollection("agg+", transform=transform, linewidth='shared', color="shared")
polygons = PolygonCollection("agg", transform=transform)

z = 0
for path in tiger.paths:
    for vertices,closed in path.vertices:
        if len(vertices) < 3:
            continue
        if path.style.stroke is not None:
            vertices[:,2] = z + 0.5
            if path.style.stroke_width:
                stroke_width = path.style.stroke_width.value
            else:
                stroke_width = 2.0
            paths.append(vertices, closed=closed, color=path.style.stroke.rgba,
                         linewidth=stroke_width)
        if path.style.fill is not None:
            if path.style.stroke is None:
                vertices[:,2] = z + 0.25
                paths.append(vertices, closed=closed, color=path.style.fill.rgba,
                             linewidth=1)
            vertices[:,2] = z
            polygons.append(vertices, color=path.style.fill.rgba)

    z += 1

window.attach(paths["transform"])
window.attach(paths["viewport"])
app.run()
