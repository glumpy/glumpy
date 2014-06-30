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

# Add an option for choosing marker
app.parser.get_default().add_argument(
    "--marker", "-m", help="Marker to display", default="ring",
    choices=("disc", "clobber", "asterisk", "infinity", "check", "T", "ring",
             "chevron-left", "chevron-right", "chevron-up", "chevron-down",
             "arrow-left", "arrow-right", "arrow-up", "arrow-down",
             "arrow2-left", "arrow2-right", "arrow2-up", "arrow2-down",
             "triangle-left", "triangle-right", "triangle-up", "triangle-down",
             "tag-left", "tag-right", "tag-up", "tag-down",
             "minus", "plus", "cross", "vbar",
             "square", "empty-square", "diamond", "empty-diamond"))

theta, phi = 0,0
window = app.Window(width=800, height=800)


n = 100000

# Parse options to get marker
options = app.parser.get_options()
marker = "shaders/markers/marker-%s.frag" % options.marker
program = gloo.Program(("shaders/markers/marker.vert",),
                       (marker, "shaders/markers/marker.frag"),n)

view = np.eye(4, dtype=np.float32)
glm.translate(view, 0, 0, -5)

program['a_position'] = 0.35 * np.random.randn(n,3)
program['a_size']   = np.random.uniform(40,60,n)
program['a_fg_color'] = 0,0,0,1
colors = np.random.uniform(0.75, 1.00, (n, 4))
colors[:,3] = 1
program['a_bg_color'] = colors
program['a_linewidth'] = 1.0
program['u_antialias'] = 1.0
program['u_model'] = np.eye(4, dtype=np.float32)
program['u_projection'] = np.eye(4, dtype=np.float32)
program['u_view'] = view
program['a_orientation'] = np.random.uniform(0, 2*np.pi, n)


@window.event
def on_draw():
    global theta, phi, translate

    theta += .5
    phi += .5
    model = np.eye(4, dtype=np.float32)
    glm.rotate(model, theta, 0, 0, 1)
    glm.rotate(model, phi, 0, 1, 0)
    program['u_model'] = model
    program['a_orientation'] += np.random.uniform(0, np.pi/256, n)

    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    program.draw(gl.GL_POINTS)

@window.event
def on_resize(width,height):
    gl.glViewport(0, 0, width, height)
    projection = glm.perspective(45.0, width / float(height), 1.0, 1000.0)
    program['u_projection'] = projection

gl.glClearColor(1.0, 1.0, 1.0, 1.0)
gl.glEnable(gl.GL_DEPTH_TEST)
gl.glEnable(gl.GL_BLEND)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
gl.glEnable(gl.GL_VERTEX_PROGRAM_POINT_SIZE)
gl.glEnable(gl.GL_POINT_SPRITE)

app.run()
