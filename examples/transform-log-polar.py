# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app
from glumpy.graphics.collections import PointCollection
from glumpy.transforms import LogScale, LinearScale, PolarProjection, Position, Viewport


window = app.Window(1024,1024, color=(1,1,1,1))

@window.event
def on_draw(dt):
    window.clear()
    points.draw()

transform = Position(PolarProjection(
    LogScale('.x', domain=(-1,3), range=(0,1)),
    LinearScale('.y', domain=(0,2*np.pi), range=(0,2*np.pi))))

points = PointCollection("agg", transform = transform)

n = 10000
R = np.random.uniform(0,1000,n)
T = np.random.uniform(0,2*np.pi,n)
Z = np.zeros(n)

points.append (np.dstack((R,T,Z)).reshape(n,3) )

window.attach(points["transform"])
window.attach(points["viewport"])
app.run()
