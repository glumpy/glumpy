#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import numpy as np
import glumpy as gp
import glumpy.gl as gl


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
    gl_Position = transform(vec4(position, 0.0, 1.0));
}
"""

fragment = """
void main()
{
    gl_FragColor = vec4(1,0,0,1);
}
"""

window = gp.Window(width=800, height=800)

@window.event
def on_draw():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    program.draw(gl.GL_TRIANGLE_STRIP)

transform = NormalizedAspect()
program = gp.gloo.Program(transform.code + vertex, fragment, count=4)
program['position'] = [(-1,-1), (-1,1), (1,-1), (1,1)]

transform.attach(program)
window.push_handlers(transform)

gp.run()
