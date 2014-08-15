#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from makecube import makecube
from glumpy import app, gl, glm, gloo
from glumpy.ext.ffmpeg_writer import FFMPEG_VideoWriter


vertex = """
uniform vec4 u_color;
uniform mat4 u_model;
uniform mat4 u_view;
uniform mat4 u_projection;

attribute vec3 position;
attribute vec4 color;

varying vec4 v_color;

void main()
{
    v_color = u_color * color;
    gl_Position = u_projection * u_view * u_model * vec4(position,1.0);
}
"""

fragment = """
varying vec4 v_color;
void main()
{
    gl_FragColor = v_color;
}
"""


width, height = 512,512
window = app.Window(width, height, color=(0.30, 0.30, 0.35, 1.00))
duration = 5.0
framerate = 60
writer = FFMPEG_VideoWriter("cube.mp4", (width, height), fps=framerate)
fbuffer = np.zeros((window.height, window.height, 3), dtype=np.uint8)


@window.event
def on_draw(dt):
    global phi, theta, writer, duration

    window.clear()

    # Filled cube
    gl.glDisable(gl.GL_BLEND)
    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glEnable(gl.GL_POLYGON_OFFSET_FILL)
    cube['u_color'] = 1, 1, 1, 1
    cube.draw(gl.GL_TRIANGLES, faces)

    # Outlined cube
    gl.glDisable(gl.GL_POLYGON_OFFSET_FILL)
    gl.glEnable(gl.GL_BLEND)
    gl.glDepthMask(gl.GL_FALSE)
    cube['u_color'] = 0, 0, 0, 1
    cube.draw(gl.GL_LINES, outline)
    gl.glDepthMask(gl.GL_TRUE)

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
    cube['u_model'] = model


@window.event
def on_resize(width, height):
    cube['u_projection'] = glm.perspective(45.0, width / float(height), 2.0, 100.0)

# Build cube data
V, I, O = makecube()
vertices = V.view(gloo.VertexBuffer)
faces    = I.view(gloo.IndexBuffer)
outline  = O.view(gloo.IndexBuffer)

cube = gloo.Program(vertex, fragment)
cube.bind(vertices)
view = np.eye(4, dtype=np.float32)
model = np.eye(4, dtype=np.float32)
projection = np.eye(4, dtype=np.float32)
glm.translate(view, 0, 0, -5)
cube['u_model'] = model
cube['u_view'] = view
phi, theta = 0, 0

# OpenGL initalization
gl.glEnable(gl.GL_DEPTH_TEST)
gl.glPolygonOffset(1, 1)
gl.glEnable(gl.GL_LINE_SMOOTH)
gl.glLineWidth(0.75)

# Run
app.run(framerate=framerate)
