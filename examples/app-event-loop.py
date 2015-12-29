# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
""" This example shows how to run the event loop manually """

from glumpy import app

window = app.Window()

@window.event
def on_draw(dt):
    window.clear()

backend = app.__backend__
clock = app.__init__(backend=backend)
count = len(backend.windows())
while count:
    count = backend.process(clock.tick())
