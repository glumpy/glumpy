#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import sys
import numpy as np

import glumpy
import glumpy.gl as gl
import glumpy.app as app
import glumpy.glm as glm
import glumpy.gloo as gloo



vertex = """
#version 120

uniform mat4 u_model;
uniform mat4 u_view;
uniform mat4 u_projection;
uniform float u_linewidth;
uniform float u_antialias;

attribute vec4  a_fg_color;
attribute vec4  a_bg_color;
attribute float a_radius;
attribute vec3  a_position;

varying float v_pointsize;
varying float v_radius;
varying vec4  v_fg_color;
varying vec4  v_bg_color;
void main (void)
{
    v_radius = a_radius;
    v_fg_color = a_fg_color;
    v_bg_color = a_bg_color;

    gl_Position = u_projection * u_view * u_model * vec4(a_position,1.0);
    gl_PointSize = 2 * (v_radius + u_linewidth + 1.5*u_antialias);
}
"""

fragment = """
#version 120

uniform float u_linewidth;
uniform float u_antialias;

varying float v_radius;
varying vec4  v_fg_color;
varying vec4  v_bg_color;
void main()
{
    float r = (v_radius + u_linewidth + 1.5*u_antialias);
    float t = u_linewidth/2.0 - u_antialias;
    float signed_distance = length(gl_PointCoord.xy - vec2(0.5,0.5)) * 2 * r - v_radius;
    float border_distance = abs(signed_distance) - t;
    float alpha = border_distance/u_antialias;
    alpha = exp(-alpha*alpha);

    // Inside shape
    if( signed_distance < 0 ) {
        // Fully within linestroke
        if( border_distance < 0 ) {
            gl_FragColor = v_fg_color;
        } else {
            gl_FragColor = mix(v_bg_color, v_fg_color, alpha);
        }
    // Outside shape
    } else {
        // Fully within linestroke
        if( border_distance < 0 ) {
            gl_FragColor = v_fg_color;
        } else if( abs(signed_distance) < (u_linewidth/2.0 + u_antialias) ) {
            gl_FragColor = vec4(v_fg_color.rgb, v_fg_color.a * alpha);
        } else {
            discard;
        }
    }
}
"""

theta, phi = 0,0
window = app.Window(width=800, height=800)


n = 1000000
program = gloo.Program(vertex, fragment, count=n)
view = np.eye(4, dtype=np.float32)
glm.translate(view, 0, 0, -5)

program['a_position'] = 0.35 * np.random.randn(n,3)
program['a_radius']   = np.random.uniform(5,10,n)
program['a_fg_color'] = 0,0,0,1
colors = np.random.uniform(0.75, 1.00, (n, 4))
colors[:,3] = 1
program['a_bg_color'] = colors
program['u_linewidth'] = 1.0
program['u_antialias'] = 1.0
program['u_model'] = np.eye(4, dtype=np.float32)
program['u_projection'] = np.eye(4, dtype=np.float32)
program['u_view'] = view

@window.event
def on_draw(dt):
    global theta, phi, translate

    program.draw(gl.GL_POINTS)

    theta += .5
    phi += .5
    model = np.eye(4, dtype=np.float32)
    glm.rotate(model, theta, 0, 0, 1)
    glm.rotate(model, phi, 0, 1, 0)
    program['u_model'] = model


@window.event
def on_resize(width,height):
    gl.glViewport(0, 0, width, height)
    projection = glm.perspective(45.0, width / float(height), 1.0, 1000.0)
    program['u_projection'] = projection

gl.glClearColor(1.0, 1.0, 1.0, 1.0)
gl.glEnable(gl.GL_DEPTH_TEST)
gl.glEnable(gl.GL_BLEND)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
gl.glEnable(gl.GL_VERTEX_PROGRAM_POINT_SIZE)
gl.glEnable(gl.GL_POINT_SPRITE)

app.run()
