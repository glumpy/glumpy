#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from makecube import makecube
from glumpy import gl, app, glm, gloo


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

quad_vertex = """
attribute vec2 position;
attribute vec2 texcoord;
varying vec2 v_texcoord;
void main()
{
    gl_Position = vec4(position, 0.0, 1.0);
    v_texcoord = texcoord;
}
"""

quad_fragment = """
uniform sampler2D texture;
varying vec2 v_texcoord;
void main()
{
    vec2 d = 5.0 * vec2(sin(v_texcoord.y*50.0),0)/512.0;
    if( v_texcoord.x > 0.5 ) {
        gl_FragColor.rgb = 1.0-texture2D(texture, v_texcoord+d).rgb;
    } else {
        gl_FragColor = texture2D(texture, v_texcoord);
    }
}
"""


def checkerboard(grid_num=8, grid_size=32):
    row_even = grid_num / 2 * [0, 1]
    row_odd = grid_num / 2 * [1, 0]
    Z = np.row_stack(grid_num / 2 * (row_even, row_odd)).astype(np.uint8)
    return 255 * Z.repeat(grid_size, axis=0).repeat(grid_size, axis=1)


window = app.Window(width=1024, height=1024)

@window.event
def on_draw():
    global phi, theta

    framebuffer.activate()
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    gl.glEnable(gl.GL_DEPTH_TEST)
    cube.draw(gl.GL_TRIANGLES, faces)
    framebuffer.deactivate()

    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    gl.glDisable(gl.GL_DEPTH_TEST)
    quad.draw(gl.GL_TRIANGLE_STRIP)

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

# Build framebuffer
w,h = window.width, window.height
depthbuffer = gloo.DepthBuffer((w,h))
colorbuffer = np.zeros((w,h,3),np.float32).view(gloo.Texture2D)
framebuffer = gloo.FrameBuffer(color=colorbuffer, depth=depthbuffer)

# Build quad
quad = gloo.Program(quad_vertex, quad_fragment, count=4)
quad['texcoord'] = [(0, 0), (0, 1), (1, 0), (1, 1)]
quad['position'] = [(-1, -1), (-1, +1), (+1, -1), (+1, +1)]
quad['texture'] = colorbuffer
quad["texture"].interpolation = gl.GL_LINEAR

# Run
app.run()
