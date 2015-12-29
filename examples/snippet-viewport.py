# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gl, glm, gloo, transforms

vertex = """
attribute vec2 position;
void main()
{
    gl_Position = vec4(position,0,1);
    <viewport.transform>;
}
"""

fragment = """
void main()
{
    <viewport.clipping>;
    gl_FragColor = vec4(1,0,0,1);
}
"""

window = app.Window(width=800, height=800)

@window.event
def on_draw(dt):
    window.clear()
    program.draw(gl.GL_TRIANGLE_STRIP)

program = gloo.Program(vertex, fragment, count=4)
program['position'] = [(-1,-1), (-1,+1), (+1,-1), (+1,+1)]

# -- Child has size of root -10 pixels
child = app.Viewport(size=(-10,-10), position=(0.5,0.5), anchor=(0.5,0.5))

# -- Child has 95% of size of root
# child = app.Viewport(size=(.95,.95), position=(0.5,0.5), anchor=(0.5,0.5), aspect=1)

# -- Child has a (fixed) size of 256x256
# child = app.Viewport(size=(256,256), position=(0.5,0.5), anchor=(0.5,0.5), aspect=1)

# -- Child is at bottom-left corner
# child = app.Viewport(size=(256,256), position=(0.0,0.0), anchor=(0.0,0.0), aspect=1)

# -- Child is at top-right corner
# child = app.Viewport(size=(256,256), position=(-1,-1), anchor=(-1,-1), aspect=1)

# -- Child is at top-right corner
# child = app.Viewport(size=(0.5,0.5), position=(-1,-1), anchor=(-1,-1), aspect=1)


@window.event
def on_resize(width,height):
    root._requested_size = width, height
    root._compute_viewport()
    program["viewport"]["global"] = root.extents
    program["viewport"]["local"] = child.extents

root = app.Viewport()
root.add(child)
program["viewport"] = transforms.Viewport()
app.run()
