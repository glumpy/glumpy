# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gl, gloo
from glumpy.transforms import Trackball, Position

vertex = """
attribute vec4 color;
attribute vec3 position;
varying vec4 v_color;
void main()
{
    gl_Position = <transform>;
    v_color = color;
}
"""
fragment = """
varying vec4 v_color;
void main()
{
    gl_FragColor = v_color;
} """


C0 = (0.75,0.75,0.75,1.00)
C1 = (1.00,0.00,0.00,0.75)
C2 = (1.00,1.00,0.00,0.75)
C3 = (0.00,0.00,1.00,0.75)

window = app.Window(1024, 1024, color = C0)

@window.event
def on_draw(dt):
    window.clear()
    quads.draw(gl.GL_TRIANGLES, indices)

@window.event
def on_init():
    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glEnable(gl.GL_BLEND)

quads = gloo.Program(vertex, fragment, count=12)
quads["position"] = [ (-1,-1,-1), (-1,+1,-1), (+1,-1,-1), (+1,+1,-1),
                      (-1,-1, 0), (-1,+1, 0), (+1,-1, 0), (+1,+1, 0),
                      (-1,-1,+1), (-1,+1,+1), (+1,-1,+1), (+1,+1,+1) ]
quads["position"] *= 10

quads["color"] = C1,C1,C1,C1, C2,C2,C2,C2, C3,C3,C3,C3
indices = np.zeros((3,6),dtype=np.uint32)
indices[0] = 0 + np.array([0,1,2,1,2,3]) 
indices[1] = 4 + np.array([0,1,2,1,2,3]) 
indices[2] = 8 + np.array([0,1,2,1,2,3]) 
indices = indices.view(gloo.IndexBuffer)

trackball = Trackball(Position("position"), znear=0.1, zfar=500, distance=50)
quads['transform'] = trackball
trackball.theta = 40
trackball.phi = 45
trackball.zoom = 40
window.attach(quads['transform'])
app.run()
