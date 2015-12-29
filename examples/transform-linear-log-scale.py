# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app
from glumpy.graphics.collections import PointCollection
from glumpy.transforms import LinearScale, LogScale, Position

window = app.Window(1024,1024, color=(1,1,1,1))

@window.event
def on_draw(dt):
    window.clear()
    points.draw()


# lin-lin
transform = Position(LinearScale('.xy', domain=(0,10)))

# log-lin
transform = Position(LogScale('.x', domain=(-1,1)),
                     LinearScale('.y', domain=(0,10)))

# lin-log
transform = Position(LinearScale('.x', domain=(0,10)),
                     LogScale('.y', domain=(-1,1)))

# log-log
# transform = Position(LogScale('.xy', domain=(-1,1)))


points = PointCollection("agg", transform = transform, color='local')
X = np.linspace(0.01,10.0,10000).reshape(10000,1)
Z = np.zeros((len(X),1))
points.append(np.hstack((X,         X, Z)), color=(1,0,0,1))
points.append(np.hstack((X, np.log(X), Z)), color=(0,1,0,1))
points.append(np.hstack((X,     10**X, Z)), color=(0,0,1,1))

window.attach(points["transform"])
window.attach(points["viewport"])
app.run()
