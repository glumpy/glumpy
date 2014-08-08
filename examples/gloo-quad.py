#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import datetime
import numpy as np
from glumpy import app, gl, gloo

vertex = """
attribute vec2 position;
void main (void)
{
    gl_Position = vec4(position, 0.0, 1.0);
}
"""

fragment = """
uniform vec3  iResolution; // Viewport resolution (in pixels)
uniform float iGlobalTime; // Shader playback time (in seconds)
void main(void)
{
    vec2 uv = gl_FragCoord.xy / iResolution.xy;
    gl_FragColor = vec4(uv, 0.5*sin(1.0+iGlobalTime), 1.0);
}
"""

window = app.Window(width=800, height=800)

@window.event
def on_draw(dt):
    window.clear()
    program.draw(gl.GL_TRIANGLE_STRIP)
    program["iGlobalTime"] += dt

@window.event
def on_resize(width, height):
    program["iResolution"] = width, height, 0

program = gloo.Program(vertex, fragment, count=4)
program['position'] = [(-1,-1), (-1,+1), (+1,-1), (+1,+1)]
gl.glClearColor(1,1,1,1)
app.run(framerate=60)
