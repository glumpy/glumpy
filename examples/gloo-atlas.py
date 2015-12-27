# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
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
        gl_FragColor = texture2D(texture, v_texcoord);
    }
"""

window = app.Window(width=800, height=800)

@window.event
def on_draw(dt):
    window.clear()
    program.draw(gl.GL_TRIANGLE_STRIP)

program = gloo.Program(vertex, fragment, count=4)
program['position'] = [(-1,-1), (-1,+1), (+1,-1), (+1,+1)]
program['texcoord'] = [( 0, 0), ( 0, 1), ( 1, 0), ( 1, 1)]


atlas = np.zeros((512,512,3),np.ubyte).view(gloo.Atlas)
program['texture'] = atlas

for i in range(400):
    height,width = np.random.randint(10,40,2)
    region = atlas.allocate((height,width))
    if region:
        x,y,width,height = region
        atlas[y:y+height,x:x+width] = np.random.randint(64,256,3)

app.run()
