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

uniform mat4  u_model;
uniform mat4  u_view;
uniform mat4  u_projection;
uniform float u_linewidth;
uniform float u_antialias;

attribute float index;
attribute vec2  P0;
attribute vec2  P1;
attribute vec4  fg_color;

varying float v_length;
varying float v_antialias;
varying float v_linewidth;
varying vec2 v_texcoord;
varying vec4 v_fg_color;

void main (void)
{
    v_antialias = u_antialias;
    v_linewidth = u_linewidth;
    v_fg_color = fg_color;

    vec2 P;
    vec2 T = P1-P0;
    v_length = length(T);
    float w = u_linewidth/2.0 + 1.5*u_antialias;
    T = w*T/v_length;

    if( index < 0.5 ) {
       P = vec2( P0.x-T.y-T.x, P0.y+T.x-T.y);
       v_texcoord = vec2(-w, +w);
    } else if( index < 1.5 ) {
       P = vec2(P0.x+T.y-T.x, P0.y-T.x-T.y);
       v_texcoord= vec2(-w, -w);
    } else if( index < 2.5 ) {
       P = vec2( P1.x-T.y+T.x, P1.y+T.x+T.y);
       v_texcoord = vec2(v_length+w, +w);
    } else {
       P = vec2( P1.x+T.y+T.x, P1.y-T.x+T.y);
       v_texcoord= vec2(v_length+w, -w);
    }

    gl_Position = u_projection * u_view * u_model * vec4(P, 0.0, 1.0);

}
"""

fragment = """
varying float v_length;
varying float v_linewidth;
varying float v_antialias;
varying vec2 v_texcoord;
varying vec4 v_fg_color;

vec4 stroke(float distance, float linewidth, float antialias, vec4 stroke)
{
    vec4 frag_color;
    float t = linewidth/2.0 - antialias;
    float signed_distance = distance;
    float border_distance = abs(signed_distance) - t;
    float alpha = border_distance/antialias;
    alpha = exp(-alpha*alpha);

    if( border_distance > (linewidth/2.0 + antialias) )
        discard;
    else if( border_distance < 0.0 )
        frag_color = stroke;
    else
        frag_color = vec4(stroke.rgb, stroke.a * alpha);

    return frag_color;
}

vec4 cap(int type, float dx, float dy,
         float linewidth, float antialias, vec4 stroke)
{
    float d = 0.0;
    dx = abs(dx);
    dy = abs(dy);
    float t = linewidth/2.0 - antialias;

    // None
    if      (type == 0)  discard;
    // Round
    else if (type == 1)  d = sqrt(dx*dx+dy*dy);
    // Triangle in
    else if (type == 3)  d = (dx+abs(dy));
    // Triangle out
    else if (type == 2)  d = max(abs(dy),(t+dx-abs(dy)));
    // Square
    else if (type == 4)  d = max(dx,dy);
    // Butt
    else if (type == 5)  d = max(dx+t,dy);

    return stroke(d, linewidth, antialias, stroke);
}


void main()
{
   if (v_texcoord.x < 0.0) {
       gl_FragColor = cap( 1, v_texcoord.x, v_texcoord.y,
                           v_linewidth, v_antialias, v_fg_color);
   } else if(v_texcoord.x > v_length) {
       gl_FragColor = cap( 1, v_texcoord.x-v_length, v_texcoord.y,
                           v_linewidth, v_antialias, v_fg_color);
   } else {
       gl_FragColor = stroke( v_texcoord.y, v_linewidth, v_antialias, v_fg_color);
   }
}
"""


window = app.Window(width=800, height=800)

@window.event
def on_draw(dt):
    program.draw(gl.GL_TRIANGLE_STRIP)

@window.event
def on_resize(width, height):
    gl.glViewport(0, 0, width, height)
    projection = glm.ortho(0, width, 0, height, -1, +1)
    program['u_projection'] = projection



program = gloo.Program(vertex, fragment, count=4)
program['u_antialias'] = 1.00
program['u_linewidth'] = 32.00
program['u_model'] = np.eye(4, dtype=np.float32)
program['u_view'] = np.eye(4, dtype=np.float32)
program['P0'] = (150,150), (150,150), (150,150), (150,150)
program['P1'] = (650,650), (650,650), (650,650), (650,650)
program['index'] = 0,1,2,3
program['fg_color'] = 0,0,0,1


gl.glClearColor(1.0, 1.0, 1.0, 1.0)
gl.glDisable(gl.GL_DEPTH_TEST)
gl.glEnable(gl.GL_BLEND)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA);
gl.glEnable(gl.GL_VERTEX_PROGRAM_POINT_SIZE)
gl.glEnable(gl.GL_POINT_SPRITE)

app.run(framerate=60)
