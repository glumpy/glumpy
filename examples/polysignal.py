#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
# Author: Cyrille Rossant
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gloo, gl, glm

vertex = """
// y coordinate of the position.
attribute float a_position;

// row, col, and time index.
attribute vec3 a_index;
varying vec3 v_index;

// 2D scaling factor (zooming).
uniform vec2 u_scale;

// Size of the table.
uniform vec2 u_size;

// Number of samples per signal.
uniform float u_n;

// Color.
attribute vec3 a_color;
varying vec4 v_color;

// Varying variables used for clipping in the fragment shader
varying vec2 v_position;
varying vec4 v_ab;

void main() {
    // Compute the x coordinate from the time index
    float x = -1.0 + 2.0*a_index.z / (u_n-1.0);
    vec2 position = vec2(x, a_position);

    // Find the affine transformation for the subplots
    vec2 a = 0.95 / u_size;
    vec2 b = vec2(-1.0 + 2.0*(a_index.x+0.5) / u_size.x,
                  -1.0 + 2.0*(a_index.y+0.5) / u_size.y);

    // Apply the static subplot transformation + scaling
    gl_Position = vec4(a*u_scale*position+b, 0.0, 1.0);

    v_color = vec4(a_color, 1.);
    v_index = a_index;

    // For clipping test in the fragment shader
    v_position = gl_Position.xy;
    v_ab = vec4(a, b);
}
"""

fragment = """
varying vec4 v_color;
varying vec3 v_index;
varying vec2 v_position;
varying vec4 v_ab;

void main() {
    // Discard the fragments between the signals
    if ((fract(v_index.x) > 0.0) || (fract(v_index.y) > 0.0))
        discard;

    // Clipping test.
    vec2 test = abs((v_position.xy-v_ab.zw)/v_ab.xy);
    if ((test.x > 1.0) || (test.y > 1.0))
        discard;

    gl_FragColor = v_color;
}
"""

# Number of cols and rows in the table.
nrows, ncols = 16, 20

# Number of signals.
m = nrows*ncols

# Number of samples per signal.
n = 1000

# Various signal amplitudes.
amplitudes = 0.1 + 0.2 * np.random.rand(m, 1).astype(np.float32)

# Generate the signals as a (m, n) array.
y = amplitudes * np.random.randn(m, n).astype(np.float32)
y = y.view(gloo.VertexBuffer)

# Color of each vertex
color = np.repeat(np.random.uniform(size=(m, 3), low=.5, high=.9),
                  n, axis=0).astype(np.float32)

# Signal 2D index of each vertex (row and col) and x-index
#  (sample index within each signal).
index = np.c_[np.repeat(np.repeat(np.arange(ncols), nrows), n),
              np.repeat(np.tile(np.arange(nrows), ncols), n),
              np.tile(np.arange(n), m)].astype(np.float32)

window = app.Window(800,600)
program = gloo.Program(vertex, fragment)
program['a_position'] = y.ravel()
program['a_color'] = color
program['a_index'] = index
program['u_scale'] = 1.0, 1.0
program['u_size'] = ncols, nrows
program['u_n'] = n

@window.event
def on_draw(dt):
    window.clear()
    program.draw(gl.GL_LINE_STRIP)
    y[:, :-10] = y[:, 10:]
    y[:, -10:] = amplitudes * np.random.randn(m, 10)

@window.event
def on_mouse_scroll(x, y, dx, dy):
    dx = np.sign(dy) * .05
    program['u_scale'] *= np.exp(2.5*dx), 1.0
    program['u_scale'][0] = max(1.0, program['u_scale'][0])

app.run()
