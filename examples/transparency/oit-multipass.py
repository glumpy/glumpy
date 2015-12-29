# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
# Weighted Blended Order-Independent Transparency.
#
# See:
#  - http://jcgt.org/published/0002/02/09/
#  - http://casual-effects.blogspot.com/2014/03/weighted-blended-order-independent.html
#  - http://casual-effects.blogspot.fr/2015/03/implemented-weighted-blended-order.html
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
    v_depth = -(<transform.trackball_view>*<transform.trackball_model>*vec4(position,1.0)).z;
    v_color = color;
}
"""

frag_quads = """
uniform float pass;
varying vec4 v_color;
varying float v_depth;
void main()
{
    float z = v_depth;
    float alpha = v_color.a;
    float weight = pow(alpha + 0.01f, 2.0f) +
                   max(0.01f, min(3000.0f, 0.3f / (0.00001f + pow(abs(z) / 200.0f, 4.0f))));
    if( pass < 0.5 )
        gl_FragData[0] = vec4(v_color.rgb * alpha, alpha) * weight;
    else
        gl_FragData[0] = vec4(alpha);
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
    vec4 opaque = vec4(0.75,0.75,0.75,1.0);
    vec4 accum = texture2D(tex_accumulation, v_texcoord);
    float r = texture2D(tex_revealage, v_texcoord).r;
    if( r == 1.0)
        discard;
    gl_FragColor = vec4(accum.rgb / max(accum.a, 0.00001), 1-r);
}
"""

C0 = (0.75, 0.75, 0.75, 1.00)
C1 = (1.00, 0.00, 0.00, 0.75)
C2 = (1.00, 1.00, 0.00, 0.75)
C3 = (0.00, 0.00, 1.00, 0.75)

window = app.Window(width=1024, height=1024, color = C0)

@window.event
def on_draw(dt):
    window.clear(color=C0)
    
    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glDepthMask(gl.GL_FALSE)
    gl.glEnable(gl.GL_BLEND)

    # Transparent surfaces

    # Pass 1: accumulation
    quads["pass"] = 0
    framebuffer.color = accumulation
    framebuffer.activate()
    gl.glBlendFunc(gl.GL_ONE,  gl.GL_ONE)
    window.clear(color=(0,0,0,0))
    quads.draw(gl.GL_TRIANGLES, indices)
    framebuffer.deactivate()

    # Pass 2: revealage
    quads["pass"] = 1
    framebuffer.color = revealage
    framebuffer.activate()
    gl.glBlendFunc(gl.GL_ZERO, gl.GL_ONE_MINUS_SRC_COLOR)
    window.clear(color=(1,1,1,1))
    quads.draw(gl.GL_TRIANGLES, indices)
    framebuffer.deactivate()
    
    # Compositing
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
    post.draw(gl.GL_TRIANGLE_STRIP)
    
    

accumulation = np.zeros((window.height,window.width,4),np.float32).view(gloo.TextureFloat2D)
revealage = np.zeros((window.height,window.width),np.ubyte).view(gloo.Texture2D)
framebuffer = gloo.FrameBuffer(color=[accumulation])

quads = gloo.Program(vert_quads, frag_quads, count=12)
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

# Post composition
post = gloo.Program(vert_post, frag_post)
post['tex_accumulation'] = accumulation
post['tex_revealage']    = revealage
post['position']  = [(-1,-1), (-1,1), (1,-1), (1,1)]

trackball = Trackball(Position("position"), znear=0.1, zfar=100.0, distance=50)
quads['transform'] = trackball
trackball.theta = 40
trackball.phi = 45
trackball.zoom = 40
window.attach(quads['transform'])

app.run()
