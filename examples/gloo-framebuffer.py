# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gl, gloo

vertex_1 = """
attribute vec2 position;
void main()
{
    gl_Position = vec4(position,0.0,1.0);
}
"""
fragment_1 = """
void main()
{
    gl_FragColor = vec4(10,10,10,1);
}
"""

vertex_2 = """
attribute vec2 position;
varying vec2 v_texcoord;
void main()
{
    gl_Position = vec4(0.85*position,0.0,1.0);
    v_texcoord = (position+1.0)/2.0;
}
"""
fragment_2 = """
uniform sampler2D texture;
varying vec2 v_texcoord;
void main()
{
    vec4 color = texture2D(texture, v_texcoord);
    gl_FragColor = color / vec4(20,20,20,1);
}
"""

window = app.Window(width=512, height=512)

@window.event
def on_draw(dt):
    window.clear()
    framebuffer.activate()
    quad_1.draw(gl.GL_TRIANGLE_STRIP)
    framebuffer.deactivate()
    quad_2.draw(gl.GL_TRIANGLE_STRIP)

texture = np.zeros((window.height,window.width,4),np.float32).view(gloo.TextureFloat2D)
framebuffer = gloo.FrameBuffer(color=[texture])
quad_1 = gloo.Program(vertex_1, fragment_1, count=4)
quad_1["position"] = (-1,-1), (-1,+1), (+1,-1), (+1,+1)
quad_2 = gloo.Program(vertex_2, fragment_2, count=4)
quad_2["position"] = (-1,-1), (-1,+1), (+1,-1), (+1,+1)
quad_2["texture"] = texture

app.run()
