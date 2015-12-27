# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
from glumpy import app, gl, gloo
from glumpy.transforms import Rotate

vertex = """
attribute vec2 position;
void main (void)
{
    gl_Position = vec4( <transform(position)>, 0.0, 1.0);
}
"""

fragment = """
void main(void)
{
    gl_FragColor = vec4(1,0,0,1);
}
"""

window = app.Window(width=800, height=800)

@window.event
def on_draw(dt):
    window.clear()
    quad.draw(gl.GL_TRIANGLE_STRIP)
    quad["transform"].angle += 1

quad = gloo.Program(vertex, fragment, count=4)
quad["position"] = [(-.5,-.5), (-.5,+.5), (+.5,-.5), (+.5,+.5)]
quad["transform"] = Rotate(angle=10, origin=(0.5,0.5,0.0))

app.run()
