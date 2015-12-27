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
varying float  v_depth;
void main()
{
    gl_Position = <transform>;
    v_depth = -(<transform.trackball_view>*<transform.trackball_model>*vec4(position,1.0)).z;
    v_texcoord = texcoord;
}
"""

teapot_frag = """
uniform sampler2D texture;
varying vec2 v_texcoord;
varying float v_depth;
void main()
{
    vec4 color = vec4(vec3(texture2D(texture, v_texcoord).r), .25);

    float z = v_depth;
    float alpha = color.a;
    float weight = pow(alpha + 0.01f, 4.0f) +
                   max(0.01f, min(3000.0f, 0.3f / (0.00001f + pow(abs(z) / 200.0f, 4.0f))));
    gl_FragData[0] = vec4(color.rgb * alpha * weight, alpha);
    gl_FragData[1].r = alpha * weight;
}
"""


post_process_vert = """
attribute vec2 position;
varying vec2 v_texcoord;
void main(void)
{
    gl_Position = vec4(position,0,1);
    v_texcoord = (position+1.0)/2.0;
}"""

post_process_frag = """
uniform sampler2D tex_accumulation;
uniform sampler2D tex_revealage;
varying vec2 v_texcoord;
void main(void)
{
    vec4 accum = texture2D(tex_accumulation, v_texcoord);
    float r = accum.a;
    accum.a = texture2D(tex_revealage, v_texcoord).r;
    if (r >= 1.0) discard;
    gl_FragColor = vec4(accum.rgb / clamp(accum.a, 1e-4, 5e4), r);
}
"""



window = app.Window(width=1024, height=1024, color=(.75,.75,.75,1))

@window.event
def on_draw(dt):

    window.clear()
    gl.glDepthMask(gl.GL_FALSE)
    gl.glEnable(gl.GL_BLEND)

    # Transparent surfaces
    framebuffer.activate()
    window.clear(color=(0,0,0,1))
    gl.glBlendFuncSeparate(gl.GL_ONE,  gl.GL_ONE,
                           gl.GL_ZERO, gl.GL_ONE_MINUS_SRC_ALPHA)
    teapot.draw(gl.GL_TRIANGLES, indices)
    framebuffer.deactivate()
    
    # Compositing
    gl.glBlendFunc(gl.GL_ONE_MINUS_SRC_ALPHA, gl.GL_SRC_ALPHA)
    gl.glEnable(gl.GL_BLEND)
    post_process.draw(gl.GL_TRIANGLE_STRIP)



accumulation = np.zeros((window.height,window.width,4),np.float32).view(gloo.TextureFloat2D)
revealage    = np.zeros((window.height,window.width),np.float32).view(gloo.TextureFloat2D)
framebuffer  = gloo.FrameBuffer(color=[accumulation,revealage])


vertices, indices = primitives.teapot()
vertices["position"] *= 10
teapot = gloo.Program(teapot_vert, teapot_frag)
teapot.bind(vertices)
teapot['texture'] = data.checkerboard()

# Post composition
post_process = gloo.Program(post_process_vert, post_process_frag)
post_process['tex_accumulation'] = accumulation
post_process['tex_revealage'] = revealage
post_process['position']  = [(-1,-1), (-1,1), (1,-1), (1,1)]

trackball = Trackball(Position("position"), znear=0.1, zfar=100.0, distance=50)
teapot['transform'] = trackball
trackball.theta = 40
trackball.phi = 135
trackball.zoom = 40

window.attach(teapot['transform'])
app.run()
