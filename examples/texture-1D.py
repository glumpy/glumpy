#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import sys
import numpy as np
from PIL import Image

import glumpy
import glumpy.gl as gl
import glumpy.app as app
import glumpy.gloo as gloo

vertex = """
    attribute vec2 position;
    attribute vec2 texcoord;
    varying vec2 v_texcoord;
    void main()
    {
        gl_Position = vec4(position, 0.0, 1.0);
        v_texcoord = texcoord;
    }
"""

fragment = """
    uniform sampler1D texture1;
    uniform sampler2D texture2;
    varying vec2 v_texcoord;
    void main()
    {
        gl_FragColor = texture1D(texture1, v_texcoord.x);
    }
"""

window = app.Window(width=512, height=512)

@window.event
def on_draw():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    program.draw(gl.GL_TRIANGLE_STRIP)

@window.event
def on_resize(width, height):
    gl.glViewport(0, 0, width, height)

program = gloo.Program(vertex, fragment, count=4)
program['position'] = [(-1,-1), (-1,+1), (+1,-1), (+1,+1)]
program['texcoord'] = [( 0, 1), ( 0, 0), ( 1, 1), ( 1, 0)]
program['texture1'] = np.linspace(0.0,1.0,256)
program['texture2'] = np.random.uniform(0.5,1.0,(64,64,3))
app.run()
