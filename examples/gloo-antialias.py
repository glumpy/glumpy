#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gl, gloo, glm, shaders

vertex = """
// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------
#version 120

// Constants
// ------------------------------------
const float SQRT_2 = 1.4142135623730951;

// Uniform
// ------------------------------------
uniform mat4  u_projection;

// Attributes
// ------------------------------------
attribute float a_size;
attribute float a_orientation;
attribute vec3  a_position;
attribute float a_antialias;
attribute float a_linewidth;
attribute vec4  a_fg_color;
attribute vec4  a_bg_color;

// Varyings
// ------------------------------------
varying float v_antialias;
varying float v_linewidth;
varying float v_size;
varying vec4  v_fg_color;
varying vec4  v_bg_color;
varying vec2  v_rotation;


// Main
// ------------------------------------
void main (void)
{
    v_size = a_size;
    v_linewidth = a_linewidth;
    v_antialias = a_antialias;
    v_fg_color = a_fg_color;
    v_bg_color = a_bg_color;
    v_rotation = vec2(cos(a_orientation), sin(a_orientation));
    gl_Position = u_projection * vec4(a_position, 1.0);
    gl_PointSize = SQRT_2 * v_size + 2.0 * (a_linewidth + 1.5*v_antialias);
}
"""

fragment = """
// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------

// Constants
// ------------------------------------
const float SQRT_2 = 1.4142135623730951;

// External functions
// ------------------------------------
float marker(vec2, float);

// Varyings
// ------------------------------------
varying vec4  v_fg_color;
varying vec4  v_bg_color;
varying float v_antialias;
varying float v_linewidth;
varying float v_size;
varying vec2  v_rotation;

// Main
// ------------------------------------
void main()
{
    vec2 P = gl_PointCoord.xy - vec2(0.5,0.5);
    P = vec2(v_rotation.x*P.x - v_rotation.y*P.y,
             v_rotation.y*P.x + v_rotation.x*P.y);
    float point_size = SQRT_2*v_size  + 2 * (v_linewidth + 1.5*v_antialias);
    float d = marker(P*point_size, v_size);
    gl_FragColor = outline(d, v_linewidth, v_antialias, v_fg_color, v_bg_color);
//    gl_FragColor = filled(d, v_linewidth, v_antialias, v_fg_color);
//    gl_FragColor = stroke(d, v_linewidth, v_antialias, v_fg_color);
}
"""


# Create window
window = app.Window(width=4*512+32, height=3*256+32, color=(1,1,1,1))

# What to draw when necessary
@window.event
def on_draw(dt):
    window.clear()
    program.draw(gl.GL_POINTS)

# Setup ortho matrix on resize
@window.event
def on_resize(width, height):
    program['u_projection'] = glm.ortho(0, width, 0, height, -1, +1)


# Setup some markers
n = 3*8
data = np.zeros(n, dtype=[('a_position',    np.float32, 3),
                          ('a_fg_color',    np.float32, 4),
                          ('a_bg_color',    np.float32, 4),
                          ('a_size',        np.float32, 1),
                          ('a_orientation', np.float32, 1),
                          ('a_antialias',   np.float32, 1),
                          ('a_linewidth',   np.float32, 1)])
data = data.view(gloo.VertexBuffer)
data['a_linewidth'] = 1
data['a_fg_color'] = 0, 0, 0, 1
data['a_bg_color'] = 1, 1, 1, 0
data['a_orientation'] = 0

radius = 256

for j in range(3):
    for i in range(8):
        x = (i+0.5)*radius
        y = (j+0.5)*radius
        index = j*8+i
        data['a_orientation'][index] = 0
        data['a_position'][index]    = x, y, 0
        data['a_size'][index]        = .75*radius
        data['a_linewidth'][index]   = 1+i*3
        data['a_antialias'][index] = 1
        if j == 2:
            data['a_antialias'][index] = 1+i*3
        elif j == 1:
            v = 0.35 + 0.5 * (i/8.0)
            data['a_fg_color'][index] = 0,0,0,1
            data['a_bg_color'][index] = 1,1,.85,1
        elif j == 0:
            v = i / 8.0
            data['a_fg_color'][index] = 0,0,0,1
            data['a_bg_color'][index] = 0,0,0,1


program = gloo.Program( vertex,
                        shaders.get("markers/marker-clobber.frag") +
                        shaders.get("antialias/outline.frag") +
                        shaders.get("antialias/stroke.frag") +
                        shaders.get("antialias/filled.frag") +
                        fragment)
program.bind(data)
app.run()
