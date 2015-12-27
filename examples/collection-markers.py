# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from  glumpy import app
from glumpy.graphics.collections import MarkerCollection


window = app.Window(1024,1024, color=(1,1,1,1))

@window.event
def on_draw(dt):
    window.clear()
    markers.draw()
    markers['orientation'] += np.random.uniform(0.0,0.1,len(markers))
    del markers[0]
    if not len(markers):
        app.quit()

n = 256
markers = MarkerCollection(orientation='local')
markers.append(np.random.uniform(-1,1,(n,3)),
               bg_color = np.random.uniform(0,1,(n,4)),
               size = 64, fg_color=(0,0,0,1))


window.attach(markers["transform"])
window.attach(markers["viewport"])
app.run()
