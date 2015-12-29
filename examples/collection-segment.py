# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, glm
from glumpy.graphics.collections import SegmentCollection
from glumpy.transforms import Position, OrthographicProjection, PanZoom

window = app.Window(width=1200, height=600, color=(1,1,1,1))

@window.event
def on_draw(dt):
    window.clear()
    segments.draw()

@window.event
def on_key_press(key, modifiers):
    if key == app.window.key.SPACE:
        transform.reset()

n = 100
P0 = np.dstack((np.linspace(100,1100,n),np.ones(n)* 50,np.zeros(n))).reshape(n,3)
P1 = np.dstack((np.linspace(110,1110,n),np.ones(n)*550,np.zeros(n))).reshape(n,3)

transform = PanZoom(OrthographicProjection(Position()))
segments = SegmentCollection(mode="agg", linewidth='local', transform=transform)
segments.append(P0, P1, linewidth = np.linspace(1, 8, n))
segments['antialias'] = 1

window.attach(segments["transform"])
window.attach(segments["viewport"])
app.run()
