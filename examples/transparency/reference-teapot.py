# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gl, gloo, data
from glumpy.geometry import primitives
from glumpy.transforms import Trackball, Position


teapot_vert = """
attribute vec3 position;
attribute vec2 texcoord;
varying vec2 v_texcoord;
void main()
{
    gl_Position = <transform>;
    v_texcoord = texcoord;
}
"""

teapot_frag = """
uniform sampler2D texture;
varying vec2 v_texcoord;
void main()
{
    gl_FragColor = vec4(vec3(texture2D(texture, v_texcoord).r), .25);
}
"""

window = app.Window(width=1024, height=1024, color=(.75,.75,.75,1))

@window.event
def on_draw(dt):
    window.clear()
    teapot.draw(gl.GL_TRIANGLES, indices)

@window.event
def on_init():
    gl.glEnable(gl.GL_BLEND)
    gl.glEnable(gl.GL_DEPTH_TEST)

vertices, indices = primitives.teapot()
vertices["position"] *= 10
teapot = gloo.Program(teapot_vert, teapot_frag)
teapot.bind(vertices)
teapot['texture'] = data.checkerboard()

trackball = Trackball(Position("position"), znear=0.1, zfar=100.0, distance=50)
teapot['transform'] = trackball
trackball.theta = 40
trackball.phi = 135
trackball.zoom = 40

window.attach(teapot['transform'])
app.run()
