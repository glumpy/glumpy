# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, glm, gl
from glumpy.graphics.collections import PolygonCollection, PathCollection
from glumpy.transforms import Position, Viewport, OrthographicProjection

window = app.Window(width=800, height=800, color=(1,1,1,1))
P = []

@window.event
def on_draw(dt):
    window.clear()
    polys.draw()
    paths.draw()

@window.event
def on_mouse_press(x, y ,button):
    global P
    P = []
    if len(paths) > 0: del paths[0]
    if len(polys) > 0: del polys[0]

@window.event
def on_mouse_release(x, y ,button):
    global P
    if len(paths) > 0: del paths[0]
    if len(polys) > 0: del polys[0]
    if len(P):
        paths.append(np.array(P),closed=True)
        polys.append(np.array(P))

@window.event
def on_mouse_drag(x, y, dx, dy, button):
    global P
    P.append( (x, window.height-y,0) )
    if len(paths) > 0: del paths[0]
    paths.append(np.array(P), closed=False)


transform = OrthographicProjection(Position())

paths = PathCollection(mode="agg", transform=transform)
polys = PolygonCollection(mode="agg", transform=transform, color="global")
paths["linewidth"] = 1.0
paths["color"] = 0.0, 0.0, 0.0, 1.00
polys["color"] = 0.0, 0.0, 0.0, 0.10

window.attach(paths["transform"])
window.attach(paths["viewport"])
app.run()
