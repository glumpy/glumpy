#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import numpy as np
import glumpy as gp
import glumpy.gl as gl
from glumpy.transforms import PanZoom, Position2D


vertex = """
    attribute vec2 position;
    attribute vec2 texcoord;
    varying vec2 v_texcoord;
    void main()
    {
        gl_Position = <transform>;
        v_texcoord = texcoord;
    }
"""

fragment = """
uniform sampler1D colormap;
varying vec2 v_texcoord;
void main()
{
    const int n = 300;
    const float log_2 = 0.6931471805599453;
    vec2 c = 3.0*v_texcoord - vec2(2.0,1.5);

    float x, y, d;
    int i;
    vec2 z = c;
    for(i = 0; i < n; ++i)
    {
        x = (z.x*z.x - z.y*z.y) + c.x;
        y = (z.y*z.x + z.x*z.y) + c.y;
        d = x*x + y*y;
        if (d > 4.0) break;
        z = vec2(x,y);
    }
    if ( i < n ) {
        float nu = log(log(sqrt(d))/log_2)/log_2;
        float index = float(i) + 1.0 - nu;
        float v = pow(index/float(n),0.5);
        gl_FragColor = texture1D(colormap, v);
    } else {
        // gl_FragColor = texture1D(colormap, 1.0);
        discard;
    }
}
"""

window = gp.Window(width=800, height=800)

@window.event
def on_draw():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    program.draw(gl.GL_TRIANGLE_STRIP)

@window.event
def on_key_press(key, modifiers):
    if key == gp.app.window.key.SPACE:
        transform.reset()

program = gp.gloo.Program(vertex, fragment, count=4)
program['position'] = [(-1,-1), (-1, 1), ( 1,-1), ( 1, 1)]
program['texcoord'] = [( 0, 1), ( 0, 0), ( 1, 1), ( 1, 0)]
colormap = np.zeros((512,3), np.float32)
colormap[:,0] = np.interp(np.arange(512), [0, 171, 342, 512], [0,1,1,1])
colormap[:,1] = np.interp(np.arange(512), [0, 171, 342, 512], [0,0,1,1])
colormap[:,2] = np.interp(np.arange(512), [0, 171, 342, 512], [0,0,0,1])
# colormap[-1] = 0,0,0

program['colormap'] = colormap
program['colormap'].interpolation = gl.GL_LINEAR

transform = PanZoom(Position2D("position"))
program['transform'] = transform
window.attach(transform)

gp.run()
