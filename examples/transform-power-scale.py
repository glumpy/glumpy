# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app
from glumpy.graphics.collections import PointCollection
from glumpy.transforms import PowerScale, Position, Viewport

window = app.Window(1024,1024, color=(1,1,1,1))

@window.event
def on_draw(dt):
    window.clear()
    points.draw()

@window.event
def on_mouse_scroll(x,y,dx,dy):
    if dy < 0:
        transform["exponent"] = np.minimum(10.0, 1.1*transform["exponent"])
    else:
        transform["exponent"] = np.maximum(0.1, transform["exponent"]/1.1)

transform = Position(PowerScale())
transform["exponent"] = 2
transform["domain"] = -10,+10

points = PointCollection("agg", transform = transform)
P = np.random.uniform(-100,100,(10000,3))
P = np.copysign(np.sqrt(abs(P)),P)
points.append(P)


window.attach(points["transform"])
window.attach(points["viewport"])
app.run()
