# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
from glumpy import app

window1 = app.Window(color=(0,0,0,1))
window2 = app.Window(color=(1,1,1,1))

@window1.event
def on_draw(dt):
    window1.clear()

@window2.event
def on_draw(dt):
    window2.clear()

app.run()
