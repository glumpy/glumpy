# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gl, glm, gloo
from glumpy.geometry import colorcube

vertex = """
uniform vec4 ucolor;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
attribute vec3 position;
attribute vec4 color;

varying vec4 v_color;

void main()
{
    v_color = ucolor * color;
    gl_Position = projection * view * model * vec4(position,1.0);
}
"""

fragment = """
varying vec4 v_color;
void main()
{
    gl_FragColor = v_color;
}
"""

window = app.Window(width=1024, height=1024, color=(0.30, 0.30, 0.35, 1.00))


@window.event
def on_draw(dt):
    global phi, theta, duration

    window.clear()

    # Filled cube
    gl.glDisable(gl.GL_BLEND)
    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glEnable(gl.GL_POLYGON_OFFSET_FILL)
    cube['ucolor'] = 1, 1, 1, 1
    cube.draw(gl.GL_TRIANGLES, faces)

    # Outlined cube
    gl.glDisable(gl.GL_POLYGON_OFFSET_FILL)
    gl.glEnable(gl.GL_BLEND)
    gl.glDepthMask(gl.GL_FALSE)
    cube['ucolor'] = 0, 0, 0, 1
    cube.draw(gl.GL_LINES, outline)
    gl.glDepthMask(gl.GL_TRUE)

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

@window.event
def on_init():
    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glPolygonOffset(1, 1)
    gl.glEnable(gl.GL_LINE_SMOOTH)
    gl.glLineWidth(0.75)

vertices, faces, outline = colorcube()
cube = gloo.Program(vertex, fragment)
cube.bind(vertices)
cube['model'] = np.eye(4, dtype=np.float32)
cube['view'] = glm.translation(0, 0, -5)
phi, theta = 0, 0

app.run()
