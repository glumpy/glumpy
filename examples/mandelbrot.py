#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
""" Mandelbrot set with pan & zoom """

import glumpy
import numpy as np
from glumpy import app, gl, glm, gloo
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
varying vec2 v_texcoord;

vec3 hot(float t)
{
    return vec3(smoothstep(0.00,0.33,t),
                smoothstep(0.33,0.66,t),
                smoothstep(0.66,1.00,t));
}

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
        gl_FragColor = vec4(hot(v),1.0);
    } else {
        gl_FragColor = vec4(hot(0.0),1.0);
    }
}
"""

window = app.Window(width=800, height=800)
console = glumpy.Console(rows=32,cols=80,color=(1,1,1,1))

@window.timer(1/30.0)
def timer(fps):
    console.clear()
    console.write("----------------------------------")
    console.write(" Glumpy version %s" % (glumpy.__version__))
    console.write(" Window size: %dx%d" % (window.width, window.height))
    console.write(" Console size: %dx%d" % (console._rows, console._cols))
    console.write(" Backend: %s (%s)" % (window._backend.__name__,
                                        window._backend.__version__))
    console.write(" Actual FPS: %.2f frames/second" % (window.fps))
    console.write("----------------------------------")

@window.event
def on_draw(dt):
    window.clear()
    program.draw(gl.GL_TRIANGLE_STRIP)
    console.draw()

@window.event
def on_key_press(key, modifiers):
    if key == app.window.key.SPACE:
        transform.reset()

program = gloo.Program(vertex, fragment, count=4)
program['position'] = [(-1,-1), (-1, 1), ( 1,-1), ( 1, 1)]
program['texcoord'] = [( 0, 1), ( 0, 0), ( 1, 1), ( 1, 0)]

transform = PanZoom(Position2D("position"))
program['transform'] = transform
window.attach(transform)
window.attach(console)
app.run()
