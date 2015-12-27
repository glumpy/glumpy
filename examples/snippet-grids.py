# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gloo, gl, glm


Position = gloo.Snippet("""
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
    float col = mod(index,cols) + 0.5;
    float row = floor(index/cols) + 0.5;
    float x = -1.0 + col * (2.0/cols);
    float y = -1.0 + row * (2.0/rows);
    float w = 0.95 / (1.0*cols);
    float h = 0.95 / (1.0*rows);
    v_x = position.x;
    v_y = position.y;
    return vec2(x + w*v_x, y + h*v_y);
}
""")

Clip = gloo.Snippet("""
varying float v_x, v_y, v_index;
void clip()
{
    if (fract(v_index) > 0.0) discard;
    if( v_x < -0.95)          discard;
    if( v_x > +0.95)          discard;
    // if( v_y < -0.95)       discard;
    // if( v_y > +0.95)       discard;
}
""")


vertex = """
attribute float index, posx, posy;
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
    Y = program["posy"].reshape(rows*cols,n)
    Y[:,:-10] = Y[:,10:]
    Y[:,-10:] = 0.5 * np.random.uniform(-1,1, (rows*cols,10))

@window.event
def on_mouse_scroll(x, y, dx, dy):
    dx = np.sign(dy) * .05
    program['xscale'] *= np.exp(2.5*dx)
    program['xscale'] = max(1.0, program['xscale'])

rows, cols, n = 16,20, 1000
program = gloo.Program(vertex, fragment)
program["index"] = np.repeat(np.arange(rows*cols),n)
program["color"] = np.repeat(np.random.uniform(0.5,0.9,(rows*cols,3)),n,axis=0)
program["posx"] = np.tile(np.linspace(-1,1,n),rows*cols)
program["posy"] = 0.5*np.random.uniform(-1,1,rows*cols*n)
program["grid"] = Position(Grid(XScale("vec2(posx,posy)"), "index"))
program["grid"]["rows"] = rows
program["grid"]["cols"] = cols
program["grid"]["xscale"] = 1.0
program["clip"] = Clip()


app.run()
