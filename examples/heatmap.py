# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gl, gloo, library
from glumpy.transforms import PanZoom, Position

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
        v_quadsize = viewport.zw * <transform.panzoom_scale>;
        v_pixcoord = texcoord * v_quadsize;
    }
"""

fragment = """
#include "markers/markers.glsl"
#include "antialias/antialias.glsl"

uniform sampler2D data;
uniform vec2 data_shape;
varying vec2 v_texcoord;
varying vec2 v_quadsize;
varying vec2 v_pixcoord;

void main()
{
    float rows = data_shape.x;
    float cols = data_shape.y;
    float v = texture2D(data, v_texcoord).r;

    vec2 size = v_quadsize / vec2(cols,rows);
    vec2 center = (floor(v_pixcoord/size) + vec2(0.5,0.5)) * size;
    float d = marker_square(v_pixcoord - center, .9*size.x);
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

n = 64
program['position'] = [(-1,-1), (-1,1), (1,-1), (1,1)]
program['texcoord'] = [( 0, 1), ( 0, 0), ( 1, 1), ( 1, 0)]
program['data'] = np.random.uniform(0,1,(n,n))
program['data_shape'] = program['data'].shape[:2]
transform = PanZoom(Position("position"),aspect=1)

program['transform'] = transform
window.attach(transform)
app.run()
