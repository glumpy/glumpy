# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
# This is a python implementation of the "Weighted Blended Order-Independent
# Transparency" technique by Morgan McGuire and Louis Bavoil
#
# This implementation use the glumpy python framework available from:
# glumpy.github.io and https://github.com/glumpy/glumpy
#
# Useful resources:
#  - http://jcgt.org/published/0002/02/09/
#  - http://casual-effects.blogspot.com/2014/03/weighted-blended-order-independent.html
#  - http://casual-effects.blogspot.fr/2015/03/implemented-weighted-blended-order.html
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gl, gloo
from glumpy.transforms import Trackball, Position

# This is the transparent scene vertex shader
# To be rendered after opaque objects widht depth writing disabled
scene_vert = """
#version 120

attribute vec4 color;
attribute vec3 position;

varying vec4 v_color;
varying float v_depth;
void main()
{
    // Transform is a simple projection*model*view*vec4(positon,1.0)
    // You can use your own
    gl_Position = <transform>;

    // Depth n eye space coordinates (model*view*vec4(positon,1.0))
    v_depth = -(<transform.trackball_view>*<transform.trackball_model>*vec4(position,1.0)).z;

    v_color = color;
}
"""

# This is the transparent scene fragment shader
# To be rendered after opaque objects widht depth writing disabled
scene_frag = """
#version 120

varying vec4 v_color;
varying float v_depth;
void main()
{
    float z = v_depth;
    float alpha = v_color.a;

    // This can be adpated depending on your scene
    // In this implementation, the 3 quads lies between -40 and -60 z coordinates
    float weight = pow(alpha + 0.01f, 4.0f) +
                   max(0.01f, min(3000.0f, 0.3f / (0.00001f + pow(abs(z) / 200.0f, 4.0f))));

    // RGBA32F texture (accumulation)
    gl_FragData[0] = vec4(v_color.rgb * alpha * weight, alpha);

    // R32F texture (revealage)
    // Make sure to use the red channel (and GL_RED target in your texture)
    gl_FragData[1].r = alpha * weight;
}
"""

# Post processing (compositing) vertex shader
compose_vert = """
#version 120

attribute vec2 position;
varying vec2 v_texcoord;
void main(void)
{
    gl_Position = vec4(position,0,1);
    v_texcoord = (position+1.0)/2.0;
}"""


# Post processing (compositing) fragment shader
compose_frag = """
#version 120

uniform sampler2D tex_accumulation;
uniform sampler2D tex_revealage;
varying vec2 v_texcoord;
void main(void)
{
    vec4 accum = texture2D(tex_accumulation, v_texcoord);
    float r = accum.a;
    accum.a = texture2D(tex_revealage, v_texcoord).r;
    if (r >= 1.0) {
        discard;
    }
    gl_FragColor = vec4(accum.rgb / clamp(accum.a, 1e-4, 5e4), r);
}
"""

C0 = 0.75, 0.75, 0.75, 1.00 # Background color
C1 = 1.00, 0.00, 0.00, 0.75 # Red quad color
C2 = 1.00, 1.00, 0.00, 0.75 # Yellow quad color
C3 = 0.00, 0.00, 1.00, 0.75 # Blue quad color

# New window with a C0 clear color
window = app.Window(width=1024, height=1024)

@window.event
def on_draw(dt):
    # Clear depth and color buffers
    gl.glClearColor(*C0)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
            
    # Opaque objects rendering
    gl.glDepthMask(gl.GL_TRUE)
    gl.glDisable(gl.GL_BLEND)
    
    # Transparent objects rendering
    gl.glDepthMask(gl.GL_FALSE)
    gl.glEnable(gl.GL_BLEND)
    framebuffer.activate()
    gl.glClearColor(0,0,0,1)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    
    window.clear(color=(0,0,0,1))
    gl.glBlendFuncSeparate(gl.GL_ONE,  gl.GL_ONE,
                           gl.GL_ZERO, gl.GL_ONE_MINUS_SRC_ALPHA)
    scene.draw(gl.GL_TRIANGLES, indices)
    framebuffer.deactivate()
    
    # Compositing
    gl.glBlendFunc(gl.GL_ONE_MINUS_SRC_ALPHA, gl.GL_SRC_ALPHA)
    compose.draw(gl.GL_TRIANGLE_STRIP)

# RGBA32F float texture
accumulation = np.zeros((window.height,window.width,4),np.float32).view(gloo.TextureFloat2D)

# R32F float texture
revealage = np.zeros((window.height,window.width),np.float32).view(gloo.TextureFloat2D)

# Framebuffer with two color targets
framebuffer = gloo.FrameBuffer(color=[accumulation,revealage])


# Three 10x10 quads at z=-10,0,+10
scene = gloo.Program(scene_vert, scene_frag, count=12)
scene["position"] = [ (-1,-1,-1), (-1,+1,-1), (+1,-1,-1), (+1,+1,-1),
                      (-1,-1, 0), (-1,+1, 0), (+1,-1, 0), (+1,+1, 0),
                      (-1,-1,+1), (-1,+1,+1), (+1,-1,+1), (+1,+1,+1) ]
scene["position"] *= 10
scene["color"] = C1,C1,C1,C1, C2,C2,C2,C2, C3,C3,C3,C3
indices = np.zeros((3,6),dtype=np.uint32)
indices[0] = 0 + np.array([0,1,2,1,2,3]) 
indices[1] = 4 + np.array([0,1,2,1,2,3]) 
indices[2] = 8 + np.array([0,1,2,1,2,3]) 
indices = indices.view(gloo.IndexBuffer)

# Post composition
compose = gloo.Program(compose_vert, compose_frag)
# Attach textures from the framebuffer
compose['tex_accumulation'] = accumulation
compose['tex_revealage']    = revealage
# Full screen quad
compose['position']  = [(-1,-1), (-1,1), (1,-1), (1,1)]

# Glumpy specific code to have a user-controlled trackball Interesting
# information is the znear/zfar and the distance. This distance is the z
# translation for the scene, hence quads final z positions are -40,-50,-60
trackball = Trackball(Position("position"), znear=0.1, zfar=100.0, distance=50)
scene['transform'] = trackball
trackball.theta = 40+100
trackball.phi = 45
trackball.zoom = 40
window.attach(scene['transform'])

app.run()
