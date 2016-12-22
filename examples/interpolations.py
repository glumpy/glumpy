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
    attribute float interpol;
    varying vec2 v_texcoord;
    varying float v_interpol;
    void main()
    {
        gl_Position = vec4(position, 0.0, 1.0);
        v_texcoord = texcoord;
        v_interpol = interpol;
    } """

fragment = """
#include "misc/spatial-filters.frag"

uniform sampler2D u_data;
uniform vec2 u_shape;
varying vec2 v_texcoord;
varying float v_interpol;
void main()
{
    if (v_interpol < 0.5)
         // gl_FragColor = Nearest(u_data, u_shape, v_texcoord);
         gl_FragColor = texture2D(u_data, v_texcoord);
    else if (v_interpol < 1.5)
        gl_FragColor = Bilinear(u_data, u_shape, v_texcoord);
    else if (v_interpol < 2.5)
        gl_FragColor = Hanning(u_data, u_shape, v_texcoord);
    else if (v_interpol < 3.5)
        gl_FragColor = Hamming(u_data, u_shape, v_texcoord);
    else if (v_interpol < 4.5)
        gl_FragColor = Hermite(u_data, u_shape, v_texcoord);
    else if (v_interpol < 5.5)
        gl_FragColor = Kaiser(u_data, u_shape, v_texcoord);
    else if (v_interpol < 6.5)
        gl_FragColor = Quadric(u_data, u_shape, v_texcoord);
    else if (v_interpol < 7.5)
        gl_FragColor = Bicubic(u_data, u_shape, v_texcoord);
    else if (v_interpol < 8.5)
        gl_FragColor = CatRom(u_data, u_shape, v_texcoord);
    else if (v_interpol < 9.5)
        gl_FragColor = Mitchell(u_data, u_shape, v_texcoord);
    else if (v_interpol < 10.5)
        gl_FragColor = Spline16(u_data, u_shape, v_texcoord);
    else if (v_interpol < 11.5)
        gl_FragColor = Spline36(u_data, u_shape, v_texcoord);
    else if (v_interpol < 12.5)
        gl_FragColor = Gaussian(u_data, u_shape, v_texcoord);
    else if (v_interpol < 13.5)
        gl_FragColor = Bessel(u_data, u_shape, v_texcoord);
    else if (v_interpol < 14.5)
        gl_FragColor = Sinc(u_data, u_shape, v_texcoord);
    else if (v_interpol < 15.5)
        gl_FragColor = Lanczos(u_data, u_shape, v_texcoord);
    else
        gl_FragColor = Blackman(u_data, u_shape, v_texcoord);
} """

window = app.Window(width=4*512, height=2*512)

@window.event
def on_draw(dt):
    window.clear()
    program.draw(gl.GL_TRIANGLES, indices)

@window.event
def on_mouse_motion(x, y, dx, dy):
    global zoom
    dx, dy = 0.05*zoom, 0.05*zoom
    x = min(max(x/1024.0, dx), 1.0-dx)
    y = min(max(y/1024.0, dy), 1.0-dy)
    vertices[1:]['texcoord'] = (x-dx,y-dy), (x-dy,y+dy), (x+dx, y-dy), (x+dx,y+dy)

@window.event
def on_mouse_scroll(x, y, dx, dy):
    global zoom
    zoom = np.minimum(np.maximum(zoom*(1+dy/100.0), 0.001), 10.00)
    on_mouse_motion(x,y,0,0)


zoom = 0.25
program = gloo.Program(vertex, fragment)
vertices = np.zeros((16+1,4),
                    [("position", np.float32, 2),
                     ("texcoord", np.float32, 2),
                     ("interpol", np.float32, 1)]).view(gloo.VertexBuffer)
vertices["position"][0] = (-1,+1), (-1,-1), (0,+1), (0,-1)
dx, dy = 1/4.0, 1/2.0
for j in range(4):
    for i in range(4):
        index = 1+j*4+i
        x, y = i/4.0, -1 + j/2.0
        vertices["position"][index] = (x,y+dy), (x,y), (x+dx,y+dy), (x+dx,y)
vertices['texcoord'] = ( 0, 0), ( 0,+1), (+1, 0), (+1,+1)
vertices['interpol'] = np.arange(17).reshape(17,1)
program.bind(vertices)
indices = np.zeros((17,6),np.uint32).view(gloo.IndexBuffer)
indices[:] = [0,1,2,1,2,3]
indices += 4*np.arange(17,dtype=np.uint32).reshape(17,1)

lena = data.get("lena.png")
program['u_data'] = lena
program['u_shape'] = lena.shape[1], lena.shape[0]
program['u_kernel'] = data.get("spatial-filters.npy")
program['u_data'].interpolation = gl.GL_NEAREST
program['u_data'].wrapping = gl.GL_CLAMP

x,y = 512,512
dx, dy = 0.05, 0.05
x = min(max(x/1024.0, dx), 1.0-dx)
y = min(max(y/1024.0, dy), 1.0-dy)
vertices['texcoord'][1:] = (x-dx,y-dy), (x-dy,y+dy), (x+dx, y-dy), (x+dx,y+dy)

app.run()
