# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gl, gloo, data
from glumpy.geometry import primitives
from glumpy.transforms import PanZoom


vertex = """
attribute vec3 position;
attribute vec2 texcoord;
varying vec2 v_texcoord;

void main()
{
    gl_Position = <transform(vec4(position.xy,0,1.0))>;
    v_texcoord = texcoord;
}
"""

fragment = """
#include "misc/spatial-filters.frag"
#include "colormaps/colormaps.glsl"

uniform sampler2D data;
uniform vec2 data_shape;
varying vec2 v_texcoord;

void main()
{
    // Extract data value
    float value = Bicubic(data, data_shape, v_texcoord).r;

    // Map value to rgb color
    vec4 bg_color = vec4(colormap_hot(value),1.0);
    vec4 fg_color = vec4(0,0,0,1);

    // Trace contour
    float levels = 32.0;

    float antialias = 1.0;
    float linewidth = 1.0 + antialias;
    if(length(value-0.5) < 0.5/levels)
        linewidth = 3.0 + antialias;

    float v  = levels*value - 0.5;
    float dv = linewidth/2.0 * fwidth(v);
    float f = abs(fract(v) - 0.5);
    float d = smoothstep(-dv,+dv,f);

    float t = linewidth/2.0 - antialias;
    d = abs(d)*linewidth/2.0 - t;
    if( d < 0.0 ) {
         gl_FragColor = bg_color;
    } else  {
        d /= antialias;
        gl_FragColor = mix(fg_color,bg_color,d);
    }
} """


window = app.Window(800, 800, color = (1,1,1,1))

@window.event
def on_draw(dt):
    window.clear()
    program.draw(gl.GL_TRIANGLES, I)

@window.event
def on_key_press(key, modifiers):
    if key == app.window.key.SPACE:
        transform.reset()

program = gloo.Program(vertex, fragment)
V,I = primitives.plane(2.0, n=64)
program.bind(V)

lena = data.get("lena.png")/256.0

program['data'] = lena[::-1,:,0]
program['data'].interpolation = gl.GL_NEAREST
program['data_shape'] = lena.shape[1], lena.shape[0]
program['u_kernel'] = data.get("spatial-filters.npy")
program['u_kernel'].interpolation = gl.GL_LINEAR

transform = PanZoom(aspect=1)
program['transform'] = transform
window.attach(transform)
app.run()
