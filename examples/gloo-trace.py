#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gl, gloo
from glumpy.transforms import Position2D, OrthographicProjection, PanZoom

# Create window
window = app.Window(width=1024, height=512)

quad_vertex = """
attribute vec2 position;
void main (void) { gl_Position = vec4(position,0,1); }
"""
quad_fragment = """
void main(void) { gl_FragColor = vec4(1,1,1,1.0/256.0); }
"""
line_vertex = """
attribute vec2 position;
void main (void) { gl_Position = vec4(position,0,1); }
"""
line_fragment = """
void main(void) { gl_FragColor = vec4(0,0,0,1); }
"""


@window.event
def on_draw(dt):
    global time

    time += np.random.uniform(0,dt)

    quad.draw(gl.GL_TRIANGLE_STRIP)
    line.draw(gl.GL_LINE_STRIP)
    window.swap()
    quad.draw(gl.GL_TRIANGLE_STRIP)
    line.draw(gl.GL_LINE_STRIP)

    X = line["position"][:,0]
    s = np.random.uniform(0.1,0.5)
    f = np.random.uniform(3,5)
    line["position"][:,1] = s*np.cos(f*X + time) + 0.01*np.random.uniform(-1,+1,n)

@window.event
def on_init():
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_DST_ALPHA)

@window.event
def on_resize(width, height):
    window.clear()
    window.swap()
    window.clear()


n = 512
line = gloo.Program(line_vertex, line_fragment, count=n)
line["position"][:,0] = np.linspace(-1,1,n)
line["position"][:,1] = np.random.uniform(-0.5,0.5,n)

quad = gloo.Program(quad_vertex, quad_fragment, count=4)
quad['position'] = [(-1,-1), (-1,+1), (+1,-1), (+1,+1)]

time = 0
app.run()
