# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
from glumpy.log import log
from glumpy import app, gl, gloo
from glumpy.graphics.text import FontManager


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

window = app.Window(width=1024, height=1024)

@window.event
def on_draw(dt):
    window.clear()
    program.draw(gl.GL_TRIANGLE_STRIP)

program = gloo.Program(vertex, fragment, count=4)
program['position'] = [(-1,-1), (-1,+1), (+1,-1), (+1,+1)]
program['texcoord'] = [( 0, 1), ( 0, 0), ( 1, 1), ( 1, 0)]
log.info("Caching texture fonts")

manager = FontManager()

for size in range(8,25):
    font = manager.get("OpenSans-Regular.ttf", size=size, mode='agg')
    font.load(""" !\"#$%&'()*+,-./0123456789:;<=>?"""
              """@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_"""
              """`abcdefghijklmnopqrstuvwxyz{|}~""")

program['texture'] = manager.atlas_agg
app.run()
