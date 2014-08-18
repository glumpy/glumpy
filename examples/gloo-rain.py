#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gloo, gl, glm

vertex = """
#version 120

uniform mat4  u_projection;
uniform float u_linewidth;
uniform float u_antialias;

attribute vec3  a_position;
attribute vec4  a_fg_color;
attribute float a_size;

varying vec4  v_fg_color;
varying float v_size;

void main (void)
{
    v_size = a_size;
    v_fg_color = a_fg_color;
    if( a_fg_color.a > 0.0)
    {
        gl_Position = u_projection * vec4(a_position,1.0);
        gl_PointSize = v_size + u_linewidth + 2*1.5*u_antialias;
    }
    else
    {
        gl_Position = u_projection * vec4(-1,-1,0,1);
        gl_PointSize = 0.0;
    }
}
"""

fragment = """
#version 120

uniform float u_linewidth;
uniform float u_antialias;
varying vec4 v_fg_color;
varying vec4 v_bg_color;
varying float v_size;
float disc(vec2 P, float size)
{
    return length((P.xy - vec2(0.5,0.5))*size);
}
void main()
{
    if( v_fg_color.a <= 0.0)
        discard;
    float actual_size = v_size + u_linewidth + 2*1.5*u_antialias;
    float t = u_linewidth/2.0 - u_antialias;
    float r = disc(gl_PointCoord, actual_size);
    float d = abs(r - v_size/2.0) - t;
    if( d < 0.0 )
    {
         gl_FragColor = v_fg_color;
    }
    else if( abs(d) > 2.5*u_antialias )
    {
         discard;
    }
    else
    {
        d /= u_antialias;
        gl_FragColor = vec4(v_fg_color.rgb, exp(-d*d)*v_fg_color.a);
    }
}
"""

window = app.Window(width=800, height=800, color=(.2,.2,.2,1))

@window.event
def on_draw(dt):
    window.clear()
    program.draw(gl.GL_POINTS)

@window.event
def on_resize(width, height):
    program['u_projection'] = glm.ortho(0, width, 0, height, -1, +1)

@window.timer(1/60.)
def timer(fps):
    global index
    data['a_fg_color'][..., 3] -= 0.01
    data['a_size'] += data['a_growth']
    _, _, w, h = gl.glGetInteger(gl.GL_VIEWPORT)
    data['a_position'][index] = np.random.uniform(0,1,2)*(w,h)
    data['a_size'][index] = 5
    data['a_growth'][index] = np.random.uniform(.5,1.5)
    data['a_fg_color'][index] = 1, 1, 1, 1
    index = (index + 1) % len(data)


dtype =  [('a_position', np.float32, 2),
          ('a_fg_color', np.float32, 4),
          ('a_size',     np.float32, 1),
          ('a_growth',   np.float32, 1)]
data = np.zeros(120,dtype).view(gloo.VertexBuffer)

index = 0
program = gloo.Program(vertex, fragment)
program.bind(data)
program['u_antialias'] = 1.00
program['u_linewidth'] = 1.00
app.run()
