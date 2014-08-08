#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
from glumpy import gl, app

window1 = app.Window()
window2 = app.Window()

@window1.event
def on_draw(dt):
    gl.glClearColor(0,0,0,1)
    window1.clear()

@window2.event
def on_draw(dt):
    gl.glClearColor(1,1,1,1)
    window2.clear()

app.run()
