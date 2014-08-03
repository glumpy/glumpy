#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import glumpy
import glumpy.gl as gl
import glumpy.app as app
import glumpy.gloo as gloo

window1 = app.Window()
window2 = app.Window()

@window1.event
def on_draw(dt):
    gl.glClearColor(0,0,0,1)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

@window2.event
def on_draw(dt):
    gl.glClearColor(1,1,1,1)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

app.run()
