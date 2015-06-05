#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gl, gloo
from glumpy.transforms import Trackball, Position

vert_quads = """
attribute vec4 color;
attribute vec3 position;
varying vec4 v_color;
void main()
{
    gl_Position = <transform>;
    v_color = color;
}
"""
frag_quads = """
varying vec4 v_color;
void main()
{
    float a = min(1.0, v_color.a) * 8.0 + 0.01;
    float b = (-gl_FragCoord.z * 0.95 + 1.0);
    float weight = clamp(a * a * a * 1e8 * b * b * b, 1e-2, 3e2);

    gl_FragData[0] = vec4(weight * v_color.rgb * v_color.a, v_color.a);
    gl_FragData[1] = vec4(weight * v_color.a);
}
"""


vert_post = """
attribute vec2 position;
varying vec2 v_texcoord;
void main(void)
{
    gl_Position = vec4(position,0,1);
    v_texcoord = (position+1.0)/2.0;
}"""

frag_post = """
const float epsilon = 0.00001;

uniform sampler2D tex_accumulation;
uniform sampler2D tex_revealage;

varying vec2 v_texcoord;

void main(void)
{
    float revealage    = texture2D(tex_revealage,    v_texcoord).a;
    vec4  accumulation = texture2D(tex_accumulation, v_texcoord);
    if (revealage == 1.0) {
        discard;
    } else {
        vec3 color = accumulation.rgb / max(accumulation.a, epsilon);
        gl_FragColor = vec4(color.rgb, revealage);
    }
}
"""

C0 = (0.75,0.75,0.75,1.00)
C1 = (1.00,0.00,0.00,0.50)
C2 = (1.00,1.00,0.00,0.50)
C3 = (0.00,0.00,1.00,0.50)

window = app.Window(width=1024, height=1024, color = C0)

@window.event
def on_draw(dt):
    window.clear()
    
    # Opaque surfaces
    # None

    # Transparent surfaces
    framebuffer.activate()
    window.clear(color=(0,0,0,1))
    gl.glDepthMask(gl.GL_FALSE)
    gl.glEnable(gl.GL_BLEND)
    gl.glBlendFuncSeparate(gl.GL_ONE,  gl.GL_ONE,
                           gl.GL_ZERO, gl.GL_ONE_MINUS_SRC_ALPHA)
    quads.draw(gl.GL_TRIANGLES, indices)
    framebuffer.deactivate()

    # Compositing
    gl.glBlendFunc(gl.GL_ONE_MINUS_SRC_ALPHA, gl.GL_SRC_ALPHA)
    post.draw(gl.GL_TRIANGLE_STRIP)
    

@window.event
def on_init():
    gl.glEnable(gl.GL_DEPTH_TEST)

# Accumulation buffer
accumulation = np.zeros((window.height,window.width,4),np.float32).view(gloo.TextureFloat2D)
accumulation.interpolation = gl.GL_NEAREST

# Revealage buffer
revealage = np.zeros((window.height,window.width,4),np.float32).view(gloo.TextureFloat2D)
revealage.interpolation = gl.GL_NEAREST

# Framebuffer
framebuffer = gloo.FrameBuffer(color=[accumulation,revealage])

# Three quads
quads = gloo.Program(vert_quads, frag_quads, count=12)
quads["position"] = [ (-1,-1,-1), (-1,+1,-1), (+1,-1,-1), (+1,+1,-1),
                      (-1,-1, 0), (-1,+1, 0), (+1,-1, 0), (+1,+1, 0),
                      (-1,-1,+1), (-1,+1,+1), (+1,-1,+1), (+1,+1,+1) ]
quads["color"] = C1,C1,C1,C1, C2,C2,C2,C2, C3,C3,C3,C3
indices = np.zeros((3,6),dtype=np.uint32)
indices[0] = 0 + np.array([0,1,2,1,2,3]) 
indices[1] = 4 + np.array([0,1,2,1,2,3]) 
indices[2] = 8 + np.array([0,1,2,1,2,3]) 
indices = indices.view(gloo.IndexBuffer)

# Post composition
post = gloo.Program(vert_post, frag_post)
post['tex_accumulation'] = accumulation
post['tex_revealage']    = revealage
post['position']  = [(-1,-1), (-1,1), (1,-1), (1,1)]

trackball = Trackball(Position("position"), znear=0.1, zfar=500.0)
quads['transform'] = trackball
trackball.theta = 40
trackball.phi = 45
trackball.zoom = 25
window.attach(quads['transform'])

app.run()
