# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import re
import numpy as np
from glumpy import app, gl, data, svg, collections
from glumpy.transforms import Position, OrthographicProjection, PanZoom, Viewport


window = app.Window(800, 800, color=(1,1,1,1))
transform = PanZoom(OrthographicProjection(Position()))


@window.event
def on_draw(dt):
    window.clear()
    paths["antialias"] = -0.5
    collections.Collection.draw(paths)
    paths["antialias"] = +1.0
    collections.Collection.draw(paths)

@window.event
def on_init():
    gl.glEnable(gl.GL_DEPTH_TEST)


paths = collections.PathCollection("agg+", transform=transform)
paths["miter_limit"] = 4.0
paths["linewidth"] = 50.0
paths["color"] = 0.0,0.0,0.0,0.5

path = svg.Path("""M 300,400
                   c   0,100  200,-100  200,0
                   c   0,100 -200,-100 -200,0 z""")
vertices, closed = path.vertices[0]
paths.append(vertices, closed=closed)

window.attach(paths["transform"])
window.attach(paths["viewport"])
app.run()
