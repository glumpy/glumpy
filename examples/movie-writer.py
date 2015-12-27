# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gl, glm, gloo, data
from glumpy.geometry import primitives
from glumpy.app.movie import record


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

@window.event
def on_draw(dt):
    global phi, theta

    window.clear()
    gl.glEnable(gl.GL_DEPTH_TEST)
    cube.draw(gl.GL_TRIANGLES, faces)

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
cube['texture'] = data.checkerboard()
phi, theta = 0, 0

duration = 5.0
framerate = 60
with record(window, "cube.mp4", fps=framerate):
    app.run(framerate=framerate, duration=duration)
