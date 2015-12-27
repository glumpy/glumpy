# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gl, gloo
from glumpy.transforms import Position, OrthographicProjection, PanZoom

vertex = """
#include "math/constants.glsl"

attribute vec2  position;
attribute float size;
attribute vec4  fg_color;
attribute vec4  bg_color;
attribute float orientation;
attribute float linewidth;
attribute float antialias;

varying float v_size;
varying vec4  v_fg_color;
varying vec4  v_bg_color;
varying vec2  v_orientation;
varying float v_antialias;
varying float v_linewidth;

void main (void)
{
    v_size        = size;
    v_linewidth   = linewidth;
    v_antialias   = antialias;
    v_fg_color    = fg_color;
    v_bg_color    = bg_color;
    v_orientation = vec2(cos(orientation), sin(orientation));

    gl_Position = <transform>;
    gl_PointSize = M_SQRT2 * size + 2.0 * (linewidth + 1.5*antialias);
}
"""

# Create window
window = app.Window(width=2*512+16, height=3*128+16, color=(1,1,1,1))

# What to draw when necessary
@window.event
def on_draw(dt):
    window.clear()
    program.draw(gl.GL_POINTS)

# Setup some markers
n = 3*8
data = np.zeros(n, dtype=[('position',    np.float32, 3),
                          ('fg_color',    np.float32, 4),
                          ('bg_color',    np.float32, 4),
                          ('size',        np.float32, 1),
                          ('orientation', np.float32, 1),
                          ('antialias',   np.float32, 1),
                          ('linewidth',   np.float32, 1)])
data = data.view(gloo.VertexBuffer)
data['linewidth'] = 1
data['fg_color'] = 0, 0, 0, 1
data['bg_color'] = 1, 1, 1, 0
data['orientation'] = 0

radius = 128

for j in range(3):
    for i in range(8):
        x = (i+0.5)*radius
        y = (j+0.5)*radius
        index = j*8+i
        data['orientation'][index] = 0
        data['position'][index]    = x, y, 0
        data['size'][index]        = .75*radius
        data['linewidth'][index]   = 1+i*2
        data['antialias'][index] = 1
        if j == 2:
            data['antialias'][index] = 1+i*3
        elif j == 1:
            v = 0.35 + 0.5 * (i/8.0)
            data['fg_color'][index] = 0,0,0,1
            data['bg_color'][index] = 1,1,.85,1
        elif j == 0:
            v = i / 8.0
            data['fg_color'][index] = 0,0,0,1
            data['bg_color'][index] = 0,0,0,1

program = gloo.Program(vertex, "markers/marker.frag")
program.bind(data)
program['marker'] = "clover"
program['paint']  = "outline"
transform = OrthographicProjection(Position("position"))
program['transform'] = transform
window.attach(transform)

app.run()
