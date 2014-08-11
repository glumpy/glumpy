#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gl, gloo, glm


# Add an option for choosing marker
app.parser.get_default().add_argument(
    "--marker", "-m", help="Marker to display", default="clobber",
    choices=("disc", "clobber", "asterisk", "infinity", "check", "T", "ring",
             "chevron-left", "chevron-right", "chevron-up", "chevron-down",
             "arrow-left", "arrow-right", "arrow-up", "arrow-down",
             "arrow2-left", "arrow2-right", "arrow2-up", "arrow2-down",
             "triangle-left", "triangle-right", "triangle-up", "triangle-down",
             "tag-left", "tag-right", "tag-up", "tag-down",
             "minus", "plus", "cross", "vbar",
             "square", "empty-square", "diamond", "empty-diamond"))


# Create window
window = app.Window(width=2*512, height=512, color=(1,1,1,1))

# What to draw when necessary
@window.event
def on_draw(dt):
    window.clear()
    program.draw(gl.GL_POINTS)
    program['a_orientation'][-1] += np.pi/1024.0

# Setup ortho matrix on resize
@window.event
def on_resize(width, height):
    projection = glm.ortho(0, width, 0, height, -1, +1)
    program['u_projection'] = projection


# Setup some markers
n = 500+1
data = np.zeros(n, dtype=[('a_position',    np.float32, 3),
                          ('a_fg_color',    np.float32, 4),
                          ('a_bg_color',    np.float32, 4),
                          ('a_size',        np.float32, 1),
                          ('a_orientation', np.float32, 1),
                          ('a_linewidth',   np.float32, 1)])
data = data.view(gloo.VertexBuffer)
data['a_linewidth'] = 1
data['a_fg_color'] = 0, 0, 0, 1
data['a_bg_color'] = 1, 1, 1, 0
data['a_orientation'] = 0
radius, theta, dtheta = 255.0, 0.0, 5.5 / 180.0 * np.pi
for i in range(500):
    theta += dtheta
    x = 256 + radius * np.cos(theta)
    y = 256 + radius * np.sin(theta)
    r = 10.1 - i * 0.02
    radius -= 0.45
    data['a_orientation'][i] = theta - np.pi/2
    data['a_position'][i] = x, y, 0
    data['a_size'][i] = 2 * r
    data['a_linewidth'][i] = 1

data['a_position'][n-1]    = 512+256, 256, 0
data['a_size'][n-1]        = 512/np.sqrt(2)
data['a_linewidth'][n-1]   = 3.0
data['a_fg_color'][n-1]    = 0, 0, 0, 1
data['a_bg_color'][n-1]    = .95, .95, .95, 1
data['a_orientation'][n-1] = 0

# Parse options to get marker
options = app.parser.get_options()
program = gloo.Program(("shaders/markers/marker.vert",),
                       ("shaders/markers/marker-%s.frag" % options.marker,
                        "shaders/markers/antialias.glsl",
                        "shaders/markers/marker.frag"))
program.bind(data)
program['u_antialias'] = 1.00
program['u_model'] = np.eye(4)
program['u_view'] = np.eye(4)
app.run()
