# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app
from glumpy.graphics.collections import PointCollection
from glumpy.transforms import LogScale, Position, Viewport

window = app.Window(1024,1024, color=(1,1,1,1))

@window.event
def on_draw(dt):
    window.clear()
    points.draw()

@window.event
def on_mouse_scroll(x,y,dx,dy):
    if dy < 0:
        transform["base"] = np.minimum(20., 1.1*transform["base"])
    else:
        transform["base"] = np.maximum(1., transform["base"]/1.1)

transform = Position(LogScale())
transform["domain"] = -1,2 # = [base^-1, base^2]
points = PointCollection("agg", transform = transform)
P = np.random.uniform(0,10,(10000,3))
points.append(P*P)

window.attach(points["transform"])
window.attach(points["viewport"])
app.run()
