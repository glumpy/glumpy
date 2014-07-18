#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import sys
import numpy as np
import glumpy
import glumpy.gl as gl
import glumpy.app as app
import glumpy.glm as glm
import glumpy.gloo as gloo

vertex = """
    attribute vec2 a_texcoord;
    attribute vec2 a_position;
    varying vec2 v_texcoord;
    void main()
    {
        gl_Position = vec4(a_position, 0.0, 1.0);
        v_texcoord = a_texcoord;
    } """

fragment = """
    uniform sampler2D u_data;
    uniform vec2 u_shape;
    varying vec2 v_texcoord;
    void main()
    {
        // gl_FragColor = Nearest(u_data, u_shape, v_texcoord);
        // gl_FragColor = Bilinear(u_data, u_shape, v_texcoord);
        // gl_FragColor = Hanning(u_data, u_shape, v_texcoord);
        // gl_FragColor = Hamming(u_data, u_shape, v_texcoord);
        // gl_FragColor = Hermite(u_data, u_shape, v_texcoord);
        // gl_FragColor = Kaiser(u_data, u_shape, v_texcoord);
        // gl_FragColor = Quadric(u_data, u_shape, v_texcoord);
        gl_FragColor = Bicubic(u_data, u_shape, v_texcoord);
        // gl_FragColor = CatRom(u_data, u_shape, v_texcoord);
        // gl_FragColor = Mitchell(u_data, u_shape, v_texcoord);
        // gl_FragColor = Spline16(u_data, u_shape, v_texcoord);
        // gl_FragColor = Spline36(u_data, u_shape, v_texcoord);
        // gl_FragColor = Gaussian(u_data, u_shape, v_texcoord);
        // gl_FragColor = Bessel(u_data, u_shape, v_texcoord);
        // gl_FragColor = Sinc(u_data, u_shape, v_texcoord);
        // gl_FragColor = Lanczos(u_data, u_shape, v_texcoord);
        // gl_FragColor = Blackman(u_data, u_shape, v_texcoord);
    } """
fragment = open('shaders/spatial-filters.frag').read() + fragment

window = app.Window(width=512, height=512)

@window.event
def on_draw():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    program.draw(gl.GL_TRIANGLE_STRIP)

@window.event
def on_resize(width, height):
    gl.glViewport(0, 0, width, height)

program = gloo.Program(vertex, fragment, count=4)
program['a_position'] = (-1,-1), (-1,+1), (+1,-1), (+1,+1)
program['a_texcoord'] = ( 0, 0), ( 0,+1), (+1, 0), (+1,+1)
data = np.random.uniform(0,1,(32,32,1))
program['u_data'] = data
program['u_shape'] = data.shape[1], data.shape[0]
program['u_data']._interpolation = gl.GL_NEAREST, gl.GL_NEAREST
program['u_kernel'] = np.load("spatial-filters.npy")

app.run()
