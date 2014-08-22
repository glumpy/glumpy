#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
from glumpy import app

window1 = app.Window(color=(0,0,0,1))
window2 = app.Window(color=(1,1,1,1))

@window1.event
def on_draw(dt): window1.clear()

@window2.event
def on_draw(dt): window2.clear()

app.run()
