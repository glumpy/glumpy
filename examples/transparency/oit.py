#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2015, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
# Weighted Blended Order-Independent Transparency.
#
# See:
#  - http://jcgt.org/published/0002/02/09/
#  - http://casual-effects.blogspot.com/2014/03/weighted-blended-order-independent.html
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gl, gloo
from glumpy.transforms import Trackball, Position

vert_quads = """
attribute vec4 color;
attribute vec3 position;
varying vec4 v_color;
varying float v_depth;
void main()
{
    gl_Position = <transform>;
    vec4 P = (<transform.trackball_view>*<transform.trackball_model>*vec4(position,1.0));
    v_depth = -P.z;
    v_color = color;
}
"""
frag_quads = """
varying vec4 v_color;
varying float v_depth;
void main()
{
    float z  = v_depth;
    float ai = v_color.a;
    vec3  Ci = v_color.rgb * ai;

    // This comes from: 
    // https://github.com/AnalyticalGraphicsInc/cesium/blob/master/Source/Shaders/Builtin/Functions/alphaWeight.glsl
//    float weight = pow(ai + 0.01, 4.0)
//                   + max(1e-2, min(3.0 * 1e3, 100.0 / (1e-5 + pow(abs(z) / 10.0, 3.0)
//                   + pow(abs(z) / 200.0, 6.0))));
//    float weight = clamp(0.5 / 1e-5 + pow(abs(z) / 200.0, 3.0), 1e-3, 3e4);
    float weight = clamp(0.5 / 1e-5 + pow(abs(z) / 200.0, 3.0), 1e-3, 3e7);


    float wzi = weight;
    gl_FragData[0] = vec4(Ci * wzi, ai);
    gl_FragData[1] = vec4(ai * wzi);
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
uniform sampler2D tex_accumulation;
uniform sampler2D tex_revealage;
varying vec2 v_texcoord;
void main(void)
{
    // See https://github.com/AnalyticalGraphicsInc/cesium/blob/master/Source/Shaders/CompositeOITFS.glsl
    vec4 opaque = vec4(0.75,0.75,0.75,0.00);
    vec4 accum = texture2D(tex_accumulation, v_texcoord);
    float r = texture2D(tex_revealage, v_texcoord).a;
    vec4 transparent = vec4(accum.rgb / clamp(r, 1e-4, 5e4), accum.a);
    gl_FragColor = (1.0 - transparent.a) * transparent + transparent.a * opaque;
}
"""

C0 = (0.75, 0.75, 0.75, 1.00)
C1 = (1.00, 0.00, 0.00, 0.75)
C2 = (1.00, 1.00, 0.00, 0.75)
C3 = (0.00, 0.00, 1.00, 0.75)

window = app.Window(width=1024, height=1024, color = (1,1,1,1))

@window.event
def on_draw(dt):
    
    # Opaque surfaces
    window.clear()

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
#                               depth=gloo.DepthBuffer(window.width,window.height))

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

trackball = Trackball(Position("position"), znear=0.1, zfar=500.0, distance=8)
quads['transform'] = trackball
trackball.theta = 40
trackball.phi = 45
trackball.zoom = 25
window.attach(quads['transform'])

app.run()
