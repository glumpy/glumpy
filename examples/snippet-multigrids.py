#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gloo, gl, glm


Position2D = gloo.Snippet("""
vec4 position2D(vec2 position)
{
    return vec4(position, 0.0, 1.0);
}
""")

XScale = gloo.Snippet("""
uniform float xscale;
vec2 scale(vec2 position)
{
    return vec2(xscale,1.0) * position;
}
""")

Grid = gloo.Snippet("""
uniform float rows, cols;
varying float v_x, v_y, v_index;
vec2 cell(vec2 position, float index)
{
    v_index = index;
    v_x = position.x;
    v_y = position.y;

    if( index < 0.0 )
        return position;

    float col = mod(index,cols) + 0.5;
    float row = floor(index/cols) + 0.5;
    float x = -1.0 + col * (2.0/cols);
    float y = -1.0 + row * (2.0/rows);
    float w = 0.99 / (1.0*cols);
    float h = 0.99 / (1.0*rows);
    return vec2(x + w*v_x, y + h*v_y);
}
""")

Clip = gloo.Snippet("""
varying float v_x, v_y, v_index;
void clip()
{
    if (fract(v_index) > 0.0) discard;
    if( v_x < -0.99)          discard;
    if( v_x > +0.99)          discard;

    // We know we are within bounds for this simple example
    // Else, this would be required
    // if( v_y < -0.99)       discard;
    // if( v_y > +0.99)       discard;
}
""")


vertex = """
attribute float index1, index2, px, py;
attribute vec3 color;
varying vec3 v_color;
void main (void)
{
    v_color = color;
    gl_Position = <grid>;
}
"""

fragment = """
varying vec3 v_color;
void main(void)
{
    <clip>;
    gl_FragColor = vec4(v_color,1);
}
"""

window = app.Window(width=800, height=600)

@window.event
def on_draw(dt):
    window.clear()
    program.draw(gl.GL_LINE_STRIP)
    Y = program["py"].reshape(m,n)
    Y[:,:-10] = Y[:,10:]
    Y[:,-10:] = 0.5 * np.random.uniform(-1,1, (m,10))

@window.event
def on_mouse_scroll(x, y, dx, dy):
    dx = np.sign(dy) * .05
    program['grid']['xscale'] *= np.exp(2.5*dx)
    program['grid']['xscale'] = max(1.0, program['grid']['xscale'])

n = 1000
rows, cols = 2,2
m = rows*cols - 1 + rows*cols # 7

program = gloo.Program(vertex, fragment)
program["index1"] = np.repeat([ 2, 2, 2, 2, 0, 1, 3],n)
program["index2"] = np.repeat([ 0, 1, 2, 3,-1,-1,-1],n)
program["color"] = np.repeat(np.random.uniform(0.5,0.9,(m,3)),n,axis=0)
program["px"]    = np.tile(np.linspace(-1,1,n),m)
program["py"]    = 0.5*np.random.uniform(-1,1,m*n)
program["grid"] = Position2D(Grid(Grid(XScale("vec2(px,py)"), "index2"), "index1"))
program["grid"]["rows"]  = rows
program["grid"]["cols"]  = cols
program["grid"]["xscale"] = 1.0
cell1 = program["grid"].args[0]
cell2 = program["grid"].args[0].args[0]
program["clip"] = Clip(**cell1.symbols) >> Clip(**cell2.symbols)

app.run()
