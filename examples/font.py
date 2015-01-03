#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
from glumpy import app
from glumpy.graphics.text import FontManager
from glumpy.graphics.collections import GlyphCollection
from glumpy.transforms import Position3D, OrthographicProjection, Viewport

window = app.Window(width=1200, height=800, color=(1,1,1,1))

@window.event
def on_draw(dt):
    window.clear()
    labels.draw()


transform = OrthographicProjection(Position3D()) + Viewport()
window.attach(transform)
labels = GlyphCollection(transform=transform)

regular = FontManager().get_file("../glumpy/data/fonts/OpenSans-Regular.ttf")
text = "The quick brown fox jumps over the lazy dog"
x,y,z = 2,window.height,0

for i in range(6,54,2):
    scale = i/48.0
    y -= i*1.1
    labels.append(text, regular, origin = (x,y,z), scale=scale, anchor_x="left")

app.run()
