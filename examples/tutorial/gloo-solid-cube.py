# -----------------------------------------------------------------------------
# Copyright (c) 2011-2016, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gl, glm, gloo

vertex = """
attribute vec3 position;
uniform mat4 model, view, projection;
void main()
{
    gl_Position = projection * view * model * vec4(position,1.0);
}
"""

fragment = """
void main()
{
    gl_FragColor = vec4(1.0,0.0,0.0,1.0);
}
"""

window = app.Window()

V = np.zeros(8, [("position", np.float32, 3)])
V["position"] = [[ 1, 1, 1], [-1, 1, 1], [-1,-1, 1], [ 1,-1, 1],
                 [ 1,-1,-1], [ 1, 1,-1], [-1, 1,-1], [-1,-1,-1]]
V = V.view(gloo.VertexBuffer)
I = np.array([0,1,2, 0,2,3,  0,3,4, 0,4,5,  0,5,6, 0,6,1,
              1,6,7, 1,7,2,  7,4,3, 7,3,2,  4,7,6, 4,6,5], dtype=np.uint32)
I = I.view(gloo.IndexBuffer)

@window.event
def on_draw(dt):
    global phi, theta
    window.clear()
    cube.draw(gl.GL_TRIANGLES, I)

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

cube = gloo.Program(vertex, fragment)
cube["position"] = V
cube['model'] = np.eye(4, dtype=np.float32)
cube['view'] = glm.translation(0, 0, -5)
phi, theta = 0, 0

app.run()
