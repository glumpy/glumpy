# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
from glumpy import app

window = app.Window()

@window.event
def on_draw(dt):
    window.clear()

app.run(framerate=60, duration=5.0)
