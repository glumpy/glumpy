#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gl
from glumpy.ext import png

window = app.Window(color=(1,0,0,1))
framebuffer = np.zeros((window.height, window.width * 3), dtype=np.uint8)

@window.event
def on_draw(dt):
    window.clear()
    gl.glReadPixels(0, 0, window.width, window.height,
                    gl.GL_RGB, gl.GL_UNSIGNED_BYTE, framebuffer)
    png.from_array(framebuffer, 'RGB').save('screenshot.png')

app.run(framecount=1)
