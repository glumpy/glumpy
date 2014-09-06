#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from  glumpy import app, gl, glm, gloo, shaders
from glumpy.transforms import Trackball, Position3D, Position2D

vertex = """
uniform vec2 iResolution;
attribute vec2 texcoord;
varying vec2 v_texcoord;
varying vec2 v_size;
void main (void)
{
    v_texcoord = texcoord;
    gl_Position = <trackball>;
}
"""

window = app.Window(width=512, height=512, color=(1,1,1,1))

@window.event
def on_draw(dt):
    window.clear()
    program.draw(gl.GL_TRIANGLE_STRIP)

@window.event
def on_resize(width, height):
    program["iResolution"] = width, height

program = gloo.Program(vertex, "./regular-grid.frag")
program["texcoord"] = (-0.5,-0.5     ), (-0.5, +0.5     ), (+0.5,-0.5    ), (+0.5,+0.5    )
program['u_major_grid_width'] = 1.5
program['u_minor_grid_width'] = 1.0
program['u_major_grid_color'] = 0, 0, 0, 1.0
program['u_minor_grid_color'] = 0, 0, 0, 0.5
program['u_antialias'] = 1.0


program['u_major_grid_step'] = np.array([ 1.00, np.pi/6])
program['u_minor_grid_step'] = np.array([ 0.25, np.pi/60])
program['u_limits1'] = -5.1, +5.1, -5.1, +5.1
program['u_limits2'] = 1.0, 5.0, 1*np.pi/6, 11*np.pi/6

program['trackball'] = Trackball(Position2D("texcoord"))
window.attach(program['trackball'])

app.run()
