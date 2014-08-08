#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
import glumpy.gl as gl
import glumpy.app as app
import glumpy.gloo as gloo


vertex = """
attribute float x, y, intensity;

varying float v_intensity;
void main (void)
{
    v_intensity = intensity;
    gl_Position = vec4(x, y, 0.0, 1.0);
}
"""

fragment = """
varying float v_intensity;
void main()
{
    gl_FragColor = vec4(0,v_intensity,0,1);
}
"""

window = app.Window(width=1024, height=512)

@window.event
def on_draw(dt):
    global index
    window.clear()
    oscilloscope.draw(gl.GL_LINE_STRIP)
    index = (index-1) % len(oscilloscope)
    oscilloscope['intensity'] -= 1.0/len(oscilloscope)
    oscilloscope['y'][index] = np.random.uniform(-0.25, +0.25)
    oscilloscope['intensity'][index] = 1.0

index = 0
oscilloscope = gloo.Program(vertex, fragment, count=150)
oscilloscope['x'] = np.linspace(-1,1,len(oscilloscope))

app.run()
