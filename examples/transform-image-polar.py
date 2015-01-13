#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gloo, gl, data
from glumpy.transforms import Position, PolarProjection, LinearScale

vertex = """
attribute vec2 position;
varying vec2 v_texcoord;
void main()
{
    gl_Position = vec4(position, 0.0, 1.0);
    v_texcoord = position;
} """
fragment = """
uniform sampler2D texture;
varying vec2 v_texcoord;

void main()
{
     vec2 uv = <projection.inverse(v_texcoord)>;
     gl_FragColor = texture2D(texture, <scale(uv)>.xy);
} """


window = app.Window(1024,1024, color=(1,1,1,1))

@window.event
def on_draw(dt):
    window.clear()
    program.draw(gl.GL_TRIANGLE_STRIP)

program = gloo.Program(vertex, fragment, count=4)
program['position'] = [(-1,-1), (-1,+1), (+1,-1), (+1,+1)]
program['texture'] = data.get("lena.png")
program['texture'].wrapping = gl.GL_REPEAT

program['projection'] = PolarProjection(
    # This translates texture coordinates to cartesian coordinates
    LinearScale('.x', name = 'x', domain=(-1, 1), range=(-1,1), call="forward"),
    LinearScale('.y', name = 'y', domain=(-1, 1), range=(-1,1), call="forward"))

program['scale'] = Position(
    # This translates cartesian coordinates (polar domains) to texture coordinates
    LinearScale('.x', name = 'x', domain=(0.2, 1.0),     range=(0,1)),
    LinearScale('.y', name = 'y', domain=(0.0, 2*np.pi), range=(0,1)))

app.run()
