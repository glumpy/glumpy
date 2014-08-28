#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gl, glm, gloo
from glumpy.geometry import primitives
from glumpy.ext.ffmpeg_writer import FFMPEG_VideoWriter


vertex = """
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

fragment = """
uniform sampler2D texture;
varying vec2 v_texcoord;
void main()
{
    float r = texture2D(texture, v_texcoord).r;
    gl_FragColor = vec4(vec3(r),1.0);
}
"""


width, height = 512,512
window = app.Window(width, height, color=(0.30, 0.30, 0.35, 1.00))
duration = 5.0
framerate = 60
writer = FFMPEG_VideoWriter("cube.mp4", (width, height), fps=framerate)
fbuffer = np.zeros((window.height, window.height, 3), dtype=np.uint8)

def checkerboard(grid_num=8, grid_size=32):
    row_even = grid_num / 2 * [0, 1]
    row_odd = grid_num / 2 * [1, 0]
    Z = np.row_stack(grid_num / 2 * (row_even, row_odd)).astype(np.uint8)
    return 255 * Z.repeat(grid_size, axis=0).repeat(grid_size, axis=1)


@window.event
def on_draw(dt):
    global phi, theta, writer, duration

    window.clear()
    gl.glEnable(gl.GL_DEPTH_TEST)
    cube.draw(gl.GL_TRIANGLES, faces)

    # Write one frame
    if writer is not None:
        if duration > 0:
            gl.glReadPixels(0, 0, window.width, window.height,
                            gl.GL_RGB, gl.GL_UNSIGNED_BYTE, fbuffer)
            writer.write_frame(fbuffer)
            duration -= dt
        else:
            writer.close()
            writer = None

    # Make cube rotate
    theta += 0.5 # degrees
    phi += 0.5 # degrees
    model = np.eye(4, dtype=np.float32)
    glm.rotate(model, theta, 0, 0, 1)
    glm.rotate(model, phi, 0, 1, 0)
    cube['model'] = model


@window.event
def on_resize(width, height):
    cube['projection'] = glm.perspective(45.0, width / float(height), 2.0, 100.0)


vertices, faces = primitives.cube()
cube = gloo.Program(vertex, fragment)
cube.bind(vertices)
view = np.eye(4, dtype=np.float32)
glm.translate(view, 0, 0, -3)
cube['view'] = view
cube['model'] = np.eye(4, dtype=np.float32)
cube['texture'] = checkerboard()
phi, theta = 0, 0

app.run(framerate=framerate)
