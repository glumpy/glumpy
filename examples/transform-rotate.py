#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gl, gloo
from glumpy.transforms import Position, Rotate

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
    program.draw(gl.GL_TRIANGLE_STRIP)
    program["transform"].angle += 1

program = gloo.Program(vertex, fragment, count=4)
program["position"] = [(-.5,-.5), (-.5,+.5), (+.5,-.5), (+.5,+.5)]
program["transform"] = Rotate(angle=10, origin=(0.5,0.5,0.0))
app.run()
