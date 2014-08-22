#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
from glumpy import app, gl, gloo, glm, data, text

window = app.Window(width=512, height=512)

@window.event
def on_draw(dt):
    window.clear()
    label.draw(x=256, y=256, color=(1,1,1,1))

font = text.TextureFont(data.get("OpenSans-Regular.ttf"), 64)
label = text.Label(u"Hello World !", font,
                   anchor_x = 'center', anchor_y = 'center')
app.run()
