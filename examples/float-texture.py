# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
# This example is used to check if float texture are working (depending on GPU):
# Only one color on screen: texture float are not working
# Several colors on screen: texture float are working
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gloo, gl

vertex = """
    attribute vec2 position;
    attribute vec2 texcoord;
    varying vec2 v_texcoord;
    void main()
    {
        gl_Position = vec4(position, 0.0, 1.0);
        v_texcoord = texcoord;
    }
"""

fragment = """
    uniform sampler2D texture;
    varying vec2 v_texcoord;
    void main()
    {
        float r = 256*texture2D(texture, v_texcoord).r;
        gl_FragColor = vec4(r,r,r,1);
    }
"""

window = app.Window(width=2*512, height=2*512)

@window.event
def on_draw(dt):
    window.clear()
    program.draw(gl.GL_TRIANGLE_STRIP)

program = gloo.Program(vertex, fragment, count=4)
program['position'] = [(-1,-1), (-1,+1), (+1,-1), (+1,+1)]
program['texcoord'] = [( 0, 1), ( 0, 0), ( 1, 1), ( 1, 0)]
T = np.linspace(0/256.0, 1/256.0, 32*32)
program['texture'] = T.astype(np.float32).reshape(32,32).view(gloo.TextureFloat2D)

app.run()
