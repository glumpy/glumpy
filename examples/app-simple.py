#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import glumpy.gl as gl
import glumpy.app as app

window = app.Window()

@window.event
def on_draw():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

app.run()
