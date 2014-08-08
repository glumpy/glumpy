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

uniform mat4  u_projection;
uniform float u_linewidth;
uniform float u_antialias;
uniform vec4  u_fg_color;
uniform vec4  u_bg_color;
attribute float a_size;
attribute vec2  a_position;

varying float v_size;
void main (void)
{
    gl_Position = u_projection * vec4(a_position, 0.0, 1.0);
    gl_PointSize = a_size + 2*(u_linewidth + 1.5*u_antialias);
    v_size = a_size;
}
"""

fragment = """
#version 120

uniform sampler2D u_texture;
uniform float u_linewidth;
uniform float u_antialias;
uniform vec4  u_fg_color;
uniform vec4  u_bg_color;
varying float v_size;

void main()
{
    float r = v_size + 2*(u_linewidth + 1.5*u_antialias);
    float signed_distance = r * (texture2D(u_texture, gl_PointCoord.xy).r - 0.5);
    float t = u_linewidth/2.0 - u_antialias;
    float border_distance = abs(signed_distance) - t;
    float alpha = border_distance/u_antialias;
    alpha = exp(-alpha*alpha);

    // Inside shape
    if( signed_distance < 0 ) {
        // Fully within linestroke
        if( border_distance < 0 ) {
            gl_FragColor = u_fg_color;
        // Within line stroke border and inside shape
        } else {
            gl_FragColor = mix(u_bg_color, u_fg_color, alpha);
        }
    // Outside shape
   } else {
        // Fully within linestroke
        if( border_distance < 0 ) {
            gl_FragColor = u_fg_color;
        // Within line stroke border
        } else if( abs(signed_distance) < (u_linewidth/2.0 + u_antialias) ) {
            gl_FragColor = vec4(u_fg_color.rgb, u_fg_color.a * alpha);
        // Oustide stroke border
        } else {
            discard;
        }
   }
}
"""


window = app.Window(width=512, height=512)

@window.event
def on_draw(dt):
    window.clear()
    program.draw(gl.GL_POINTS)

@window.event
def on_resize(width, height):
    gl.glViewport(0, 0, width, height)
    projection = glm.ortho(0, width, 0, height, -1, +1)
    program['u_projection'] = projection

program = gloo.Program(vertex, fragment, count=1)
program['a_position']  = 256,256
program['a_size']      = 2*256
program['u_fg_color']  = 0.00, 0.00, 0.00, 1.00
program['u_bg_color']  = 1.00, 1.00, 0.75, 1.00
program['u_antialias'] = 2* 1.00
program['u_linewidth'] = 2* 2.00

program['u_texture'] = np.load("tools/star-sdf.npy")
program['u_texture']._interpolation = gl.GL_LINEAR, gl.GL_LINEAR

gl.glClearColor(1.0, 1.0, 1.0, 1.0)
gl.glDisable(gl.GL_DEPTH_TEST)
gl.glEnable(gl.GL_BLEND)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA);
gl.glEnable(gl.GL_VERTEX_PROGRAM_POINT_SIZE)
gl.glEnable(gl.GL_POINT_SPRITE)

app.run()
