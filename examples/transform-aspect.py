#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import numpy as np
import glumpy as gp
import glumpy.gl as gl
from glumpy.transforms import LinearScale, Position2D

class NormalizedAspect(gp.transforms.LinearScale):
    """ A Linear scale transform that keep aspect ratio constant (=1) """

    def on_resize(self, width, height):
        aspect = float(width)/float(height)
        if aspect > 1.0:
            self.scale = 1.0/aspect, 1.0, 1.0
        else:
            self.scale = 1.0, aspect/1.0, 1.0


vertex = """
attribute vec2 position;
void main()
{
    gl_Position = <transform>;
}
"""

fragment = """
uniform vec4 color;
void main()
{
    gl_FragColor = color;
}
"""

window = gp.Window(width=800, height=800)

@window.event
def on_draw(dt):
    window.clear()
    program1.draw(gl.GL_TRIANGLE_STRIP)
    program2.draw(gl.GL_TRIANGLE_STRIP)

transform = NormalizedAspect(Position2D("position"))

program1 = gp.gloo.Program(vertex, fragment, count=4)
program1['position'] = [(-1,-1), (-1,1), (1,-1), (1,1)]
program1['color'] = 1,0,0,1
program1['transform'] = transform

program2 = gp.gloo.Program(vertex, fragment, count=4)
program2['position'] = [(-.5,-.5), (-.5,.5), (.5,-.5), (.5,.5)]
program2['color'] = 0,0,1,1
program2['transform'] = transform

window.attach(transform)

gp.run()
