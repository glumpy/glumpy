# -----------------------------------------------------------------------------
# Copyright (c) 2011-2016, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License. 
# -----------------------------------------------------------------------------
from glumpy import app, gl, gloo

vertex = """
attribute vec2 position;
void main (void)
{
    gl_Position = vec4(0.85*position, 0.0, 1.0);
}
"""

fragment = """
void main(void)
{
    gl_FragColor = vec4(1.0,1.0,0.0,1.0);
}
"""

window = app.Window(width=800, height=800)

@window.event
def on_draw(dt):
    window.clear()
    quad.draw(gl.GL_TRIANGLE_STRIP)

quad = gloo.Program(vertex, fragment, count=4)
quad['position'] = [(-1,-1), (-1,+1), (+1,-1), (+1,+1)]
app.run()
