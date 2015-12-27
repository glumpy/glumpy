# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from  glumpy import app, gl, glm, gloo
from glumpy.transforms import OrthographicProjection, Position


vertex = """
attribute vec2 position;
void main()
{
    gl_Position = <transform>;
}
"""

fragment = """
void main()
{
    gl_FragColor = vec4(1,0,0,1);
}
"""

window = app.Window(width=800, height=800)

@window.event
def on_draw(dt):
    window.clear()
    quad.draw(gl.GL_TRIANGLE_STRIP)

@window.event
def on_resize(w, h):
    quad['position'] = [(w-100,h-100), (w-100,h), (w,h-100), (w,h)]

quad = gloo.Program(vertex, fragment, count=4)
quad["transform"] = OrthographicProjection(Position("position"))
window.attach(quad["transform"])
app.run()
