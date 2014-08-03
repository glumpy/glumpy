#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import glumpy.gl as gl
import glumpy.app as app
import glumpy.text as text

window = app.Window(width=512, height=512)

@window.event
def on_draw(dt):
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    label.draw(x=256, y=256, color=(1,1,1,1))

font = text.TextureFont("Vera.ttf", 64)
label = text.Label(u"Hello World !", font,
                   anchor_x = 'center', anchor_y = 'center')
app.run()
