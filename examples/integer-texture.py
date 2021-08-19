# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
# This example is used to check if int texture are working (depending on GPU):
# Only one color on screen: texture int are not working
# Several colors on screen: texture int are working
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gloo, gl

vertex = """
    in vec2 position;
    in vec2 texcoord;
    out vec2 v_texcoord;
    void main()
    {
        gl_Position = vec4(position, 0.0, 1.0);
        v_texcoord = texcoord;
    }
"""

fragment = """
    uniform isampler2D tex;
    in vec2 v_texcoord;
    out vec4 fragColor;

    void main()
    {
        float c = int(texture(tex, v_texcoord).x);
        fragColor = vec4(c / 256, c / 256, c / 256, 1);
    }
"""

app.use('glfw', api='GL', major=3, minor=3, profile='core')
window = app.Window(width=512, height=512)

@window.event
def on_draw(dt):
    window.clear()
    program.draw(gl.GL_TRIANGLE_STRIP)

program = gloo.Program(vertex, fragment, count=4, version="330")
dtype = [('position', np.float32, 2),
         ('texcoord', np.float32, 2)]
array = np.zeros(4, dtype).view(gloo.VertexArray)
array['position'] = [(-1,-1), (-1,+1), (+1,-1), (+1,+1)]
array['texcoord'] = [( 0, 1), ( 0, 0), ( 1, 1), ( 1, 0)]
program.bind(array)

T = np.linspace(0, 256.0, 32*32).reshape(32, 32, 1).astype(np.int32)
program['tex'] = T.view(gloo.TextureInteger2D)

app.run()
