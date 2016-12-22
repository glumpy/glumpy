# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import gl, app, gloo


vertex = """
attribute vec2 a_position;
void main() {
    gl_Position = vec4(a_position, 0.0, 1.0);
    gl_PointSize = 30.0;
}
"""

fragment1 = """
void main() {
    gl_FragColor = vec4(0.0, 0.0, 1.0, 1.0);
}
"""

fragment2 = """
void main() {
    gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
}
"""


program1 = gloo.Program(vertex, fragment1)  # blue on the right
program1['a_position'] = np.zeros((1,2),dtype=np.float32) + 0.5
program2 = gloo.Program(vertex, fragment2)  # red on the left
program2['a_position'] = np.zeros((1,2),dtype=np.float32) - 0.5


window = app.Window()
@window.event
def on_draw(dt):
    window.clear()
    program1.draw(gl.GL_POINTS)
    program2.draw(gl.GL_POINTS)

app.run()
