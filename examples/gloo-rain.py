# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gloo, gl, glm

vertex = """
#version 120

uniform mat4  projection;
uniform float linewidth;
uniform float antialias;

attribute vec3  position;
attribute vec4  color;
attribute float size;

varying vec4  v_color;
varying float v_size;

void main (void)
{
    v_size = size;
    v_color = color;
    gl_Position = projection * vec4(position,1.0);
    gl_PointSize = size + linewidth + 2*1.5*antialias;
}
"""

fragment = """
#version 120

uniform float linewidth;
uniform float antialias;
varying vec4 v_color;
varying float v_size;

float disc(vec2 P, float size)
{
    return length((P.xy - vec2(0.5,0.5))*size);
}

void main()
{
    if( v_color.a <= 0.0)
        discard;

    float actual_size = v_size + linewidth + 2*1.5*antialias;
    float t = linewidth/2.0 - antialias;
    float r = disc(gl_PointCoord, actual_size);
    float d = abs(r - v_size/2.0) - t;
    if( d < 0.0 )
    {
         gl_FragColor = v_color;
    }
    else if( abs(d) > 2.5*antialias )
    {
         discard;
    }
    else
    {
        d /= antialias;
        gl_FragColor = vec4(v_color.rgb, exp(-d*d)*v_color.a);
    }
}
"""

window = app.Window(width=800, height=800, color=(.2,.2,.2,1))

@window.event
def on_draw(dt):
    window.clear()
    program.draw(gl.GL_POINTS)

@window.event
def on_resize(width, height):
    program['projection'] = glm.ortho(0, width, 0, height, -1, +1)

@window.timer(1/60.)
def timer(fps):
    global index
    data['color'][..., 3] -= 0.01
    data['size'] += data['growth']
    _, _, w, h = gl.glGetInteger(gl.GL_VIEWPORT)
    data['position'][index] = np.random.uniform(0,1,2)*(w,h)
    data['size'][index] = 5
    data['growth'][index] = np.random.uniform(.5,1.5)
    data['color'][index] = 1, 1, 1, 1
    index = (index + 1) % len(data)

dtype =  [('position', np.float32, 2),
          ('color',    np.float32, 4),
          ('size',     np.float32, 1),
          ('growth',   np.float32, 1)]
data = np.zeros(120,dtype).view(gloo.VertexBuffer)

index = 0
program = gloo.Program(vertex, fragment)
program.bind(data)
program['antialias'] = 1.00
program['linewidth'] = 1.00
app.run()
