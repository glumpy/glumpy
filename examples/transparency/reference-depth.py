# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gl, gloo
from glumpy.transforms import Trackball, Position

vertex = """
attribute vec3 position;
varying float depth;
void main()
{
    gl_Position = <transform>;
    vec4 p  = <transform.trackball_view>*<transform.trackball_model>*vec4(position,1.0);
    depth = -p.z/100;
}
"""
fragment = """
varying float depth;
void main()
{
    gl_FragColor = vec4(vec3(depth),1);
} """


color = (0.75,0.75,0.75,1.00)
window = app.Window(1024, 1024, color = color)

@window.event
def on_draw(dt):
    window.clear()
    quads.draw(gl.GL_TRIANGLES, indices)

@window.event
def on_init():
    gl.glEnable(gl.GL_DEPTH_TEST)


quads = gloo.Program(vertex, fragment, count=12)
quads["position"] = [ (-1,-1,-1), (-1,+1,-1), (+1,-1,-1), (+1,+1,-1),
                      (-1,-1, 0), (-1,+1, 0), (+1,-1, 0), (+1,+1, 0),
                      (-1,-1,+1), (-1,+1,+1), (+1,-1,+1), (+1,+1,+1) ]
quads["position"] *= 10
indices = np.zeros((3,6),dtype=np.uint32)
indices[0] = 0 + np.array([0,1,2,1,2,3]) 
indices[1] = 4 + np.array([0,1,2,1,2,3]) 
indices[2] = 8 + np.array([0,1,2,1,2,3]) 
indices = indices.view(gloo.IndexBuffer)

trackball = Trackball(Position("position"), znear=0.1, zfar=100, distance=50)

quads['transform'] = trackball
trackball.theta = 40
trackball.phi = 45
trackball.zoom = 25
window.attach(quads['transform'])
app.run()
