#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import sys
import numpy as np
from PIL import Image

import glumpy
import glumpy.gl as gl
import glumpy.app as app
import glumpy.glm as glm
import glumpy.gloo as gloo


vertex = """
#version 120

// Uniform
// ------------------------------------
uniform mat4  u_projection;
uniform float u_antialias;

// Attributes
// ------------------------------------
attribute float a_size;
attribute float a_orientation;
attribute float a_linewidth;
attribute vec3  a_position;
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

void main (void)
{
    v_size = a_size;
    v_linewidth = 2.5*a_linewidth;
    v_antialias = 3.0*u_antialias;
    v_fg_color = a_fg_color;
    v_bg_color = a_bg_color;
    v_rotation = vec2(cos(a_orientation), sin(a_orientation));

    gl_Position = u_projection * vec4(a_position, 1.0);
    gl_PointSize = a_size + 2*(a_linewidth + 1.5*v_antialias);
}
"""

fragment = """
#version 120

// Constants
// ------------------------------------
const float SQRT_2 = 1.4142135623730951;

// Uniforms
// ------------------------------------
uniform sampler2D u_texture;
uniform vec2 u_texture_shape;

// Varyings
// ------------------------------------
varying float v_antialias;
varying float v_linewidth;
varying vec4  v_fg_color;
varying vec4  v_bg_color;
varying float v_size;
varying vec2  v_rotation;

vec4 Nearest(sampler2D u_data, vec2 u_shape, vec2 v_texcoord);
vec4 Bilinear(sampler2D u_data, vec2 u_shape, vec2 v_texcoord);
vec4 Hanning(sampler2D u_data, vec2 u_shape, vec2 v_texcoord);
vec4 Hamming(sampler2D u_data, vec2 u_shape, vec2 v_texcoord);
vec4 Hermite(sampler2D u_data, vec2 u_shape, vec2 v_texcoord);
vec4 Kaiser(sampler2D u_data, vec2 u_shape, vec2 v_texcoord);
vec4 Quadric(sampler2D u_data, vec2 u_shape, vec2 v_texcoord);
vec4 Bicubic(sampler2D u_data, vec2 u_shape, vec2 v_texcoord);
vec4 CatRom(sampler2D u_data, vec2 u_shape, vec2 v_texcoord);
vec4 Mitchell(sampler2D u_data, vec2 u_shape, vec2 v_texcoord);
vec4 Spline16(sampler2D u_data, vec2 u_shape, vec2 v_texcoord);
vec4 Spline36(sampler2D u_data, vec2 u_shape, vec2 v_texcoord);
vec4 Gaussian(sampler2D u_data, vec2 u_shape, vec2 v_texcoord);
vec4 Bessel(sampler2D u_data, vec2 u_shape, vec2 v_texcoord);
vec4 Sinc(sampler2D u_data, vec2 u_shape, vec2 v_texcoord);
vec4 Lanczos(sampler2D u_data, vec2 u_shape, vec2 v_texcoord);
vec4 Blackman(sampler2D u_data, vec2 u_shape, vec2 v_texcoord);

void main()
{
    vec2 P = gl_PointCoord.xy - vec2(0.5,0.5);
    P = vec2(v_rotation.x*P.x - v_rotation.y*P.y,
             v_rotation.y*P.x + v_rotation.x*P.y);
    P += vec2(0.5,0.5);

    float r = v_size + 2*(v_linewidth + 1.5*v_antialias);
    // float signed_distance = r * (texture2D(u_texture, P).r - 0.5);
    float signed_distance = r * (Bicubic(u_texture, u_texture_shape, P).r - 0.5);
    float t = v_linewidth/2.0 - v_antialias;
    float border_distance = abs(signed_distance) - t;
    float alpha = border_distance/v_antialias;
    alpha = exp(-alpha*alpha);


    // Within linestroke
    if( border_distance < 0 )
        gl_FragColor = v_fg_color;
    else if( signed_distance < 0 )
        // Inside shape
        if( border_distance > (v_linewidth/2.0 + v_antialias) )
            gl_FragColor = v_bg_color;
        else // Line stroke interior border
            gl_FragColor = mix(v_bg_color,v_fg_color,alpha);
    else
        // Outide shape
        if( border_distance > (v_linewidth/2.0 + v_antialias) )
            discard;
        else // Line stroke exterior border
            gl_FragColor = vec4(v_fg_color.rgb, v_fg_color.a * alpha);
}
"""


window = app.Window(width=2*512, height=512)

@window.event
def on_draw():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    program.draw(gl.GL_POINTS)
    program["a_orientation"][-1] += np.pi/1024.0

@window.event
def on_resize(width, height):
    gl.glViewport(0, 0, width, height)
    projection = glm.ortho(0, width, 0, height, -1, +1)
    program['u_projection'] = projection


# Setup some markers
n = 500+1
data = np.zeros(n, dtype=[('a_position',    np.float32, 3),
                          ('a_fg_color',    np.float32, 4),
                          ('a_bg_color',    np.float32, 4),
                          ('a_size',        np.float32, 1),
                          ('a_orientation', np.float32, 1),
                          ('a_linewidth',   np.float32, 1)])
data = data.view(gloo.VertexBuffer)
data['a_linewidth'] = 2
data['a_fg_color'] = 0, 0, 0, 1
data['a_bg_color'] = 1, 1, 1, 1
data['a_orientation'] = 0
radius, theta, dtheta = 255.0, 0.0, 5.5 / 180.0 * np.pi
for i in range(500):
    theta += dtheta
    x = 256 + radius * np.cos(theta)
    y = 256 + radius * np.sin(theta)
    r = 10.1 - i * 0.02
    radius -= 0.45
    data['a_orientation'][i] = theta
    data['a_position'][i] = x, y, 0
    data['a_size'][i] = 1.5*r
    data['a_linewidth'][i] = 1

data['a_position'][n-1]    = 512+256, 256, 0
data['a_size'][n-1]        = 512/np.sqrt(2)
data['a_linewidth'][n-1]   = 3.0
data['a_fg_color'][n-1]    = 0, 0, 0, 1
data['a_bg_color'][n-1]    = .95, .95, .95, 1
data['a_orientation'][n-1] = 0

program = gloo.Program(vertex, ("spatial-filters.frag",fragment))
# program['u_texture'] = np.load("tools/star-sdf.npy")
program['u_texture'] = np.load("tools/octoface-sdf.npy")
program['u_texture']._interpolation = gl.GL_NEAREST, gl.GL_NEAREST
program['u_texture_shape'] = program['u_texture'].width, program['u_texture'].height
program['u_kernel'] = np.load("spatial-filters.npy")
program['u_antialias'] = 1.0
program.bind(data)

gl.glClearColor(1.0, 1.0, 1.0, 1.0)
gl.glDisable(gl.GL_DEPTH_TEST)
gl.glEnable(gl.GL_BLEND)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA);
gl.glEnable(gl.GL_VERTEX_PROGRAM_POINT_SIZE)
gl.glEnable(gl.GL_POINT_SPRITE)

app.run()
