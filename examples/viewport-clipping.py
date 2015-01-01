#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gl, gloo, library
from glumpy.graphics.collections import PointCollection
from glumpy.transforms import Transform

vertex = """
attribute vec2 position;
uniform vec4 local_viewport;
uniform vec4 global_viewport;

vec4 viewport_transform(vec4 position)
{
    float w = local_viewport.z / global_viewport.z;
    float h = local_viewport.w / global_viewport.w;
    float x = 2.0*(local_viewport.x / global_viewport.z) - 1.0 + w;
    float y = 2.0*(local_viewport.y / global_viewport.w) - 1.0 + h;
    return  vec4((x + w*position.x/position.w)*position.w,
                 (y + h*position.y/position.w)*position.w,
                 position.z, position.w);
}

void main() {
    gl_Position = vec4(position,0,1);
    gl_Position = viewport_transform(gl_Position);
} """

fragment = """
uniform vec4 color;
uniform vec4 local_viewport;
uniform vec4 global_viewport;

void viewport_clipping(void)
{
    vec2 position = gl_FragCoord.xy;
         if( position.x < (local_viewport.x)) discard;
    else if( position.x > (local_viewport.x+local_viewport.z)) discard;
    else if( position.y < (local_viewport.y)) discard;
    else if( position.y > (local_viewport.y+local_viewport.w)) discard;
}

void main() {
    viewport_clipping();
    gl_FragColor = color;
} """

window = app.Window(width=800, height=800, color=(1,1,1,1))
program = gloo.Program(vertex, fragment, count=4)
program['position'] = [(-1,-1), (-1,+1), (+1,-1), (+1,+1)]

vp0 = app.Viewport()
window.attach(vp0)
vp1 = app.Viewport(size=(.75,.75),position=(0.0,0.0), anchor=(0.0,0.0), aspect=1)
vp0.add(vp1)
vp2 = app.Viewport(size=(.75,.75),position=(0.5,0.5), anchor=(0.5,0.5), aspect=1)
vp1.add(vp2)
vp3 = app.Viewport(size=(.75,.75),position=(1.0,1.0), anchor=(1.0,1.0), aspect=1)
vp2.add(vp3)


@window.event
def on_draw(dt):
    window.clear()
    program["global_viewport"] = 0,0,window.width,window.height

    program["local_viewport"] = vp1.viewport
    program["color"] = 1.0, 0.0, 0.0, 1.0
    program.draw(gl.GL_TRIANGLE_STRIP)

    program["local_viewport"] = vp2.viewport
    program["color"] = 0.0, 1.0, 0.0, 1.0
    program.draw(gl.GL_TRIANGLE_STRIP)

    program["local_viewport"] = vp3.viewport
    program["color"] = 0.0, 0.0, 1.0, 1.0
    program.draw(gl.GL_TRIANGLE_STRIP)


app.run()
