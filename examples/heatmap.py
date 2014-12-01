#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gl, gloo, glm, shaders
from glumpy.transforms import PanZoom, Position2D


vertex = """
    uniform vec4 viewport;

    attribute vec2 position;
    attribute vec2 texcoord;

    varying vec2 v_texcoord;
    varying vec2 v_pixcoord;
    varying vec2 v_quadsize;

    void main()
    {
        gl_Position = <transform>;
        v_texcoord = texcoord;
        v_quadsize = viewport.zw * scale;
        v_pixcoord = texcoord * v_quadsize;
    }
"""

fragment = """
uniform sampler2D texture;
varying vec2 v_texcoord;
varying vec2 v_quadsize;
varying vec2 v_pixcoord;


vec4 filled(float distance, float linewidth, float antialias, vec4 fill)
{
    vec4 frag_color;
    float t = linewidth/2.0 - antialias;
    float signed_distance = distance;
    float border_distance = abs(signed_distance) - t;
    float alpha = border_distance/antialias;
    alpha = exp(-alpha*alpha);
    if( border_distance < 0.0 )
        frag_color = fill;
    else if( signed_distance < 0.0 )
        frag_color = fill;
    else
        frag_color = vec4(fill.rgb, alpha * fill.a);
    return frag_color;
}

float marker(vec2 P, float size)
{
    return max(abs(P.x), abs(P.y)) - size/2.0;
}

void main()
{
    const float rows = 32.0;
    const float cols = 32.0;

    float v = texture2D(texture, v_texcoord).r;
    vec2 size = v_quadsize / vec2(cols,rows);
    vec2 center = (floor(v_pixcoord/size) + vec2(0.5,0.5)) * size;
    float d = marker(v_pixcoord - center, 0.9*size.x);
    gl_FragColor = filled(d, 1.0, 1.0, vec4(v,v,v,1));
}
"""

window = app.Window(width=1024, height=1024, color=(1,1,1,1))

@window.event
def on_draw(dt):
    window.clear()
    program.draw(gl.GL_TRIANGLE_STRIP)

@window.event
def on_key_press(key, modifiers):
    if key == app.window.key.SPACE:
        transform.reset()

@window.event
def on_resize(width, height):
    program['viewport'] = 0, 0, width, height

program = gloo.Program(vertex, fragment, count=4)
program['position'] = [(-1,-1), (-1,1), (1,-1), (1,1)]
program['texcoord'] = [( 0, 1), ( 0, 0), ( 1, 1), ( 1, 0)]
program['texture'] = np.random.uniform(0,1,(32,32))

transform = PanZoom(Position2D("position"))
program['transform'] = transform
window.attach(transform)

app.run()
