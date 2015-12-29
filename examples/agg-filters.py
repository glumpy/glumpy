# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
""" This example shows spatial interpolation of images. """
import numpy as np
from glumpy import app, gl, gloo, data, library

vertex = """
    attribute vec2 position;
    attribute vec2 texcoord;
    varying vec2 v_texcoord;
    void main()
    {
        gl_Position = vec4(position, 0.0, 1.0);
        v_texcoord = texcoord;
    } """

fragment = """
#include "misc/spatial-filters.frag"

uniform sampler2D u_data;
uniform vec2      u_shape;
uniform float     u_interpolation;
varying vec2      v_texcoord;
void main()
{
    if (u_interpolation < 0.5)       gl_FragColor = Nearest(u_data, u_shape, v_texcoord);
    else if (u_interpolation < 1.5)  gl_FragColor = Bilinear(u_data, u_shape, v_texcoord);
    else if (u_interpolation < 2.5)  gl_FragColor = Hanning(u_data, u_shape, v_texcoord);
    else if (u_interpolation < 3.5)  gl_FragColor = Hamming(u_data, u_shape, v_texcoord);
    else if (u_interpolation < 4.5)  gl_FragColor = Hermite(u_data, u_shape, v_texcoord);
    else if (u_interpolation < 5.5)  gl_FragColor = Kaiser(u_data, u_shape, v_texcoord);
    else if (u_interpolation < 6.5)  gl_FragColor = Quadric(u_data, u_shape, v_texcoord);
    else if (u_interpolation < 7.5)  gl_FragColor = Bicubic(u_data, u_shape, v_texcoord);
    else if (u_interpolation < 8.5)  gl_FragColor = CatRom(u_data, u_shape, v_texcoord);
    else if (u_interpolation < 9.5)  gl_FragColor = Mitchell(u_data, u_shape, v_texcoord);
    else if (u_interpolation < 10.5) gl_FragColor = Spline16(u_data, u_shape, v_texcoord);
    else if (u_interpolation < 11.5) gl_FragColor = Spline36(u_data, u_shape, v_texcoord);
    else if (u_interpolation < 12.5) gl_FragColor = Gaussian(u_data, u_shape, v_texcoord);
    else if (u_interpolation < 13.5) gl_FragColor = Bessel(u_data, u_shape, v_texcoord);
    else if (u_interpolation < 14.5) gl_FragColor = Sinc(u_data, u_shape, v_texcoord);
    else if (u_interpolation < 15.5) gl_FragColor = Lanczos(u_data, u_shape, v_texcoord);
    else                             gl_FragColor = Blackman(u_data, u_shape, v_texcoord);
} """

window = app.Window(width=2*512, height=2*512)

@window.event
def on_draw(dt):
    window.clear()
    program.draw(gl.GL_TRIANGLE_STRIP)

@window.event
def on_key_press(key, modifiers):
    names = [
        "Nearest", "Bilinear", "Hanning", "Hamming",
        "Hermite", "Kaiser", "Quadric", "Bicubic",
        "CatRom", "Mitchell", "Spline16", "Spline36",
        "Gaussian", "Bessel", "Sinc", "Lanczos", "Blackman"]
    
    if key == app.window.key.RIGHT:
        program['u_interpolation'] = (program['u_interpolation'] + 1) % 17
    elif key == app.window.key.LEFT:
        program['u_interpolation'] = (program['u_interpolation'] - 1) % 17
    print("Interpolation :", names[int(program['u_interpolation'])])
    
program = gloo.Program(vertex, fragment, count=4)
program["position"] = (-1,-1), (-1,+1), (+1,-1), (+1,+1)
program['texcoord'] = ( 0, 0), ( 0,+1), (+1, 0), (+1,+1)

program['u_data'] =np.array( [ [0.0,0.0,0.0,0.0,0.0],
                               [0.0,0.5,0.5,0.5,0.0],
                               [0.0,0.5,1.0,0.5,0.0],
                               [0.0,0.5,0.5,0.5,0.0],
                               [0.0,0.0,0.0,0.0,0.0] ]).astype(np.float32)

program['u_data'].interpolation = gl.GL_NEAREST
program['u_data'].wrapping = gl.GL_CLAMP
program['u_shape'] = program['u_data'].shape[:2]

program['u_kernel'] = data.get("spatial-filters.npy")
program['u_kernel'].interpolation = gl.GL_NEAREST
program['u_kernel'].wrapping = gl.GL_CLAMP

program['u_interpolation'] = 0


app.run()
