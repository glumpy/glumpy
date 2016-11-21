# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015, Vispy Development Team. All Rights Reserved.
# Copyright (c) 2015, Dzhelil Rufat. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
"""
Illustrate how to plot a 2D function (an image) y=f(x,y) on the GPU.
"""

from glumpy import app, gl, gloo

vertex = """
attribute vec2 a_position;
varying vec2 v_position;
void main()
{
    gl_Position = vec4(a_position, 0.0, 1.0);
    v_position = a_position;
}
"""

fragment = """
#include "math/constants.glsl"
#include "colormaps/jet.glsl"
uniform float u_time;
varying vec2 v_position;

/**********************************************************
Specify the parameters here.
**********************************************************/
const float z_offset = 1.; // (z+z_offset)/z_max should be in [0,1]
const float z_max    = 2.;
const float x_scale  = 5.; // x is between -x_scale and +x_scale
const float y_scale  = 5.; // y is between -y_scale and +y_scale
const float t_scale  = 5.; // scale for the time
/*********************************************************/

// x is in [-x_scale, +x_scale]
// y is in [-y_scale, +y_scale]
// t is in [0, +oo)


float f(float x, float y, float t) {

    float k = .25*cos(t);
    return (cos(x)+k)*(sin(y)-k);

}

void main() {

    vec2 pos = v_position;
    float z = f(x_scale * pos.x, y_scale * pos.y, t_scale * u_time);
    vec3 c = colormap_jet((z + z_offset) / (z_max));
    gl_FragColor = vec4(c, 1.0);

}
"""

program = gloo.Program(vertex, fragment)
program['a_position'] = [(-1., -1.), (-1., +1.),
                         (+1., -1.), (+1., +1.)]
program['u_time'] = 0.0

window = app.Window(width=800, height=800)


@window.event
def on_draw(dt):
    program.draw(gl.GL_TRIANGLE_STRIP)
    program['u_time'] += dt


app.run()
