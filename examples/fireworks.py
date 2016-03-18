# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
"""
Example demonstrating simulation of fireworks using point sprites.
(adapted from the "OpenGL ES 2.0 Programming Guide")
"""
import numpy as np
from glumpy import app, gl, gloo

vertex = """
#version 120
uniform float time;
uniform vec2 center;
attribute vec2 start, end;
attribute float lifetime;
varying float v_lifetime;
void main () {
    gl_Position = vec4(start + (time * end) + center, 0.0, 1.0);
    gl_Position.y -= 1.0 * time * time;
    v_lifetime = clamp(1.0 - (time / lifetime), 0.0, 1.0);
    gl_PointSize = (v_lifetime * v_lifetime) * 30.0;
}
"""

fragment = """
#version 120
const float SQRT_2 = 1.4142135623730951;
uniform vec4 color;
varying float v_lifetime;
void main()
{
    gl_FragColor = color * (SQRT_2/2.0 - length(gl_PointCoord.xy - 0.5));
    gl_FragColor.a *= v_lifetime;
}
"""

n = 2500
window = app.Window(512,512)
program = gloo.Program(vertex, fragment, count=n)

def explosion():
    program['center'] = np.random.uniform(-0.5,+0.5)
    program['color'] = np.random.uniform(0.1,0.9,4)
    program['color'][3] = 1.0 / n ** 0.05
    program['lifetime'] = np.random.normal(4.0, 0.5, n)
    program['start'] = np.random.normal(0.0, 0.2, (n,2))
    program['end'] = np.random.normal(0.0, 1.2, (n,2))
    program['time'] = 0

@window.event
def on_init():
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE)

@window.event
def on_draw(dt):
    window.clear()
    program.draw(gl.GL_POINTS)
    program['time'] += dt
    if program['time'] > 1.75:
        explosion()

explosion()
app.run(framerate=60)
