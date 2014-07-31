#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from makecube import makecube
from glumpy import gl, app, glm, gloo, filters


cube_vertex = """
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
attribute vec3 position;
attribute vec2 texcoord;
varying vec2 v_texcoord;
void main()
{
    gl_Position = projection * view * model * vec4(position,1.0);
    v_texcoord = texcoord;
}
"""

cube_fragment = """
uniform sampler2D texture;
varying vec2 v_texcoord;
void main()
{
    float r = texture2D(texture, v_texcoord).r;
    gl_FragColor = vec4(vec3(r),1.0);
}
"""


def checkerboard(grid_num=8, grid_size=32):
    row_even = grid_num / 2 * [0, 1]
    row_odd = grid_num / 2 * [1, 0]
    Z = np.row_stack(grid_num / 2 * (row_even, row_odd)).astype(np.uint8)
    return 255 * Z.repeat(grid_size, axis=0).repeat(grid_size, axis=1)


window = app.Window(1024,1024)

# See http://rastergrid.com/blog/2010/09/efficient-gaussian-blur-with-linear-sampling/
VBlur = gloo.Snippet("""
vec4 filter(sampler2D original, sampler2D filtered, vec2 texcoord, vec2 texsize)
{
    return 0.2270270270 *  texture2D( filtered, texcoord)
         + 0.3162162162 * (texture2D( filtered, texcoord + vec2(0.0, 1.3846153846)/texsize) +
                           texture2D( filtered, texcoord - vec2(0.0, 1.3846153846)/texsize) )
         + 0.0702702703 * (texture2D( filtered, texcoord + vec2(0.0, 3.2307692308)/texsize) +
                           texture2D( filtered, texcoord - vec2(0.0, 3.2307692308)/texsize) );
}""")

HBlur = gloo.Snippet("""
vec4 filter(sampler2D original, sampler2D filtered, vec2 texcoord, vec2 texsize)
{
    return 0.2270270270 *  texture2D( filtered, texcoord)
         + 0.3162162162 * (texture2D( filtered, texcoord + vec2(1.3846153846, 0.0)/texsize) +
                           texture2D( filtered, texcoord - vec2(1.3846153846, 0.0)/texsize) )
         + 0.0702702703 * (texture2D( filtered, texcoord + vec2(3.2307692308, 0.0)/texsize) +
                           texture2D( filtered, texcoord - vec2(3.2307692308, 0.0)/texsize) );
}""")
GaussianBlur = filters.Filter(512, 512, VBlur, HBlur)



@window.event
def on_draw():
    global phi, theta

    with GaussianBlur:
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glEnable(gl.GL_DEPTH_TEST)
        cube.draw(gl.GL_TRIANGLES, faces)

    theta += 0.5 # degrees
    phi += 0.5 # degrees
    model = np.eye(4, dtype=np.float32)
    glm.rotate(model, theta, 0, 0, 1)
    glm.rotate(model, phi, 0, 1, 0)
    cube['model'] = model


@window.event
def on_resize(width, height):
    gl.glViewport(0, 0, width, height)
    cube['projection'] = glm.perspective(45.0, width / float(height), 2.0, 100.0)


# Build cube data
V, I, O = makecube()
vertices = V.view(gloo.VertexBuffer)
faces    = I.view(gloo.IndexBuffer)
outline  = O.view(gloo.IndexBuffer)

# Build cube
cube = gloo.Program(cube_vertex, cube_fragment)
cube.bind(vertices)
view = np.eye(4, dtype=np.float32)
glm.translate(view, 0, 0, -5)
cube['view'] = view
cube['model'] = np.eye(4, dtype=np.float32)
cube['texture'] = checkerboard()
phi, theta = 0, 0

# Run
app.run()
