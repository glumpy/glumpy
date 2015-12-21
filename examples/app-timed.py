# -----------------------------------------------------------------------------
# Copyright (c) 2011-2016, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
from glumpy import app

window = app.Window()

@window.event
def on_draw(dt):
    window.clear()

app.run(framerate=60, duration=5.0)
