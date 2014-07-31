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
uniform mat4 model, view, projection;
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


pixelate = gloo.Snippet(
"""
uniform float level;
vec4 filter(sampler2D original, sampler2D filtered, vec2 texcoord, vec2 texsize)
{
    vec2 uv = (texcoord * level);
    uv = (uv - fract(uv)) / level;
    return texture2D(filtered, uv);
} """)
sepia = gloo.Snippet(
"""
vec4 filter(vec4 color)
{
    return vec4( dot(color.rgb, vec3(.393, .769, .189)),
                 dot(color.rgb, vec3(.349, .686, .168)),
                 dot(color.rgb, vec3(.272, .534, .131)),
                 color.a );
}
vec4 filter(sampler2D original, sampler2D filtered, vec2 texcoord, vec2 texsize)
{
    return filter( texture2D(filtered, texcoord) );
}
 """)

compose = filters.Filter(512,512, sepia(pixelate))
compose["level"] = 256.0


window = app.Window(1024,1024)

@window.event
def on_draw():
    global phi, theta

    with compose:
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glEnable(gl.GL_DEPTH_TEST)
        cube.draw(gl.GL_TRIANGLES, faces)
    theta += 0.5
    phi += 0.5
    model = np.eye(4, dtype=np.float32)
    glm.rotate(model, theta, 0, 0, 1)
    glm.rotate(model, phi, 0, 1, 0)
    cube['model'] = model


@window.event
def on_resize(width, height):
    gl.glViewport(0, 0, width, height)
    cube['projection'] = glm.perspective(45.0, width / float(height), 2.0, 100.0)
    pixelate.viewport = 0, 0, width, height

@window.event
def on_mouse_scroll(x, y, dx, dy):
    p = compose["level"]
    compose["level"] = min(max(8, p + .01 * dy * p), 512)


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
app.run()
