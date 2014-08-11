#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gl, Console, __version__


window = app.Window(width=800, height=600)
console = Console(rows=24,cols=80)

@window.event
def on_draw(dt):
    window.clear(), console.draw()

@window.timer(1/30.0)
def timer(fps):
    console.clear()
    console.write("--------------------------------------------------")
    console.write("Glumpy version %s" % (__version__))
    console.write("Window size: %dx%d" % (window.width, window.height))
    console.write("Console size: %dx%d" % (console._rows, console._cols))
    console.write("Backend: %s (%s)" % (window._backend.__name__,
                                        window._backend.__version__))
    console.write("Actual FPS: %.2f frames/second" % (app.fps()))
    console.write("--------------------------------------------------")

window.attach(console)
gl.glClearColor(1,1,1,1)
app.run()
