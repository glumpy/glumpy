#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import numpy as np
from PIL import Image

from galaxy import Galaxy
from specrend import *

import glumpy
import glumpy.gl as gl
import glumpy.app as app
import glumpy.glm as glm
import glumpy.gloo as gloo


vertex = """
#version 120
uniform mat4  u_model;
uniform mat4  u_view;
uniform mat4  u_projection;
uniform sampler1D u_colormap;

attribute float a_size;
attribute float a_type;
attribute vec2  a_position;
attribute float a_temperature;
attribute float a_brightness;

varying vec3 v_color;
void main (void)
{
    gl_Position = u_projection * u_view * u_model * vec4(a_position,0.0,1.0);
    if (a_size > 2.0)
    {
        gl_PointSize = a_size;
    } else {
        gl_PointSize = 0.0;
    }
    v_color = texture1D(u_colormap, a_temperature).rgb * a_brightness;
    if (a_type == 2)
        v_color *= vec3(2,1,1);
    else if (a_type == 3)
        v_color = vec3(.9);
}
"""

fragment = """
#version 120
uniform sampler2D u_texture;
varying vec3 v_color;
void main()
{
    gl_FragColor = texture2D(u_texture, gl_PointCoord);
    gl_FragColor.rgb *= v_color;
}
"""

window = app.Window(width=800, height=800)

@window.event
def on_draw(dt):
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    galaxy.update(100000) # in years !
    program['a_size'] = galaxy['size']
    program['a_position'] = galaxy['position'] / 13000.0
    program.draw(gl.GL_POINTS)

@window.event
def on_resize(width,height):
    gl.glViewport(0, 0, width, height)
    projection = glm.perspective(45.0, width/float(height), 1.0, 1000.0)
    program['u_projection'] = projection

galaxy = Galaxy(35000)
galaxy.reset(13000, 4000, 0.0004, 0.90, 0.90, 0.5, 200, 300)
t0, t1 = 1000.0, 10000.0
n = 256
dt =  (t1-t0)/n
colors = np.zeros((n,3), dtype=np.float32)
for i in range(n):
    temperature = t0 + i*dt
    x,y,z = spectrum_to_xyz(bb_spectrum, temperature)
    r,g,b = xyz_to_rgb(SMPTEsystem, x, y, z)
    r = min((max(r,0),1))
    g = min((max(g,0),1))
    b = min((max(b,0),1))
    colors[i] = norm_rgb(r, g, b)


program = gloo.Program(vertex, fragment, count=len(galaxy))

view = np.eye(4, dtype=np.float32)
model = np.eye(4, dtype=np.float32)
projection = np.eye(4, dtype=np.float32)
glm.translate(view, 0, 0, -5)
program['u_model'] = model
program['u_view'] = view
program['u_colormap'] = colors
program['u_texture'] = np.array(Image.open("particle.png"))
program['a_temperature'] = (galaxy['temperature'] - t0) / (t1-t0)
program['a_brightness'] = galaxy['brightness']
program['a_size'] = galaxy['size']
program['a_type'] = galaxy['type']


# OpenGL initalization
# --------------------------------------
gl.glClearColor(0.0, 0.0, 0.03, 1.0)
gl.glDisable(gl.GL_DEPTH_TEST)
gl.glEnable(gl.GL_BLEND)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE);
gl.glEnable(gl.GL_VERTEX_PROGRAM_POINT_SIZE)
gl.glEnable(gl.GL_POINT_SPRITE)

# Start
# --------------------------------------
app.run(framerate=60)
