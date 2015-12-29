# -----------------------------------------------------------------------------
# Copyright (c) 2015, Dzhelil S. Rufat. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np

from glumpy import app, gloo, gl
import triangle

A = dict(vertices=np.array(((-1, -1), (1, -1), (1, 1), (-1, 1))))
B = triangle.triangulate(A, 'qa0.01')
vertices = B['vertices']
indices = B['triangles']

vertex = '''
    attribute vec2 a_position;
    void main()
    {
        gl_Position = vec4(a_position, 0.0, 1.0);
    }
'''

fragment = '''
    void main()
    {
        gl_FragColor = vec4(0.0, 0.0, 0.0, 1.0);
    }
'''

program = gloo.Program(vertex, fragment)
program['a_position'] = vertices

window = app.Window(width=512, height=512, color=(1, 1, 1, 1))


@window.event
def on_draw(_):
    window.clear()
    gl.glLineWidth(2)
    gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
    gl.glEnable(gl.GL_LINE_SMOOTH)
    program.draw(gl.GL_TRIANGLES, indices.reshape(-1).astype(np.uint32).view(gloo.IndexBuffer))


app.run()
