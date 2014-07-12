#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
import glumpy
import glumpy.gl as gl
import glumpy.app as app
import glumpy.glm as glm
import glumpy.gloo as gloo

transform = "hammer.glsl"
vertex    = "grid.vert"
fragment  = "grid.frag"


def find_closest_direct(I, start, end, count):
    Q = (I-start)/(end-start)*count
    mid = ((Q[1:]+Q[:-1]+1)/2).astype(np.int)
    boundary = np.zeros(count, np.int)
    boundary[mid] = 1
    return np.add.accumulate(boundary)

def update_grid():
    """ Grid reference update """
    n = Z.shape[1]

    xmin, xmax = limits2[:2]
    t1 = major_grid[0]
    t2 = minor_grid[0]
    I3 = np.linspace(xmin, xmax, (xmax-xmin)/t1+1, endpoint=True)
    Z[..., 0] = I3[find_closest_direct(I3, start=xmin, end=xmax, count=n)]
    I4 = np.linspace(xmin, xmax, (xmax-xmin)/t2+1, endpoint=True)
    Z[..., 1] = I4[find_closest_direct(I4, start=xmin, end=xmax, count=n)]

    ymin, ymax = limits2[2:]
    t1 = major_grid[1]
    t2 = minor_grid[1]
    I1 = np.linspace(ymin, ymax, (ymax-ymin)/t1+1, endpoint=True)
    Z[..., 2] = I1[find_closest_direct(I1, start=ymin, end=ymax, count=n)]
    I2 = np.linspace(ymin, ymax, (ymax-ymin)/t2+1, endpoint=True)
    Z[..., 3] = I2[find_closest_direct(I2, start=ymin, end=ymax, count=n)]

    program['u_grid'][...] = Z



window = app.Window(width=1024, height=1024)

@window.event
def on_draw():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    program.draw(gl.GL_TRIANGLE_STRIP)

@window.event
def on_resize(width, height):
    gl.glViewport(0, 0, width, height)

    aspect = 1.0
    if width < aspect*height:
        w,h = width, aspect*width
        x,y = 0, (height - h)/2.0
    else:
        w,h = height/aspect, height
        x,y = (width - w)/2.0, 0

    program['a_size'] = w,h
    program['a_position'] = (x, y), (x, y+h), (x+w, y), (x+w, y+h)
    program['u_projection'] = glm.ortho(0, width, 0, height, -1, +1)
    update_grid()

program = gloo.Program(vertex, [transform,fragment], 4)
program['u_model']      = np.eye(4)
program['u_view']       = np.eye(4)
program['u_projection'] = np.eye(4)

w,h = window.width, window.height
program['a_position'] = (0, 0), (0, h), (w, 0), (w, h)
program['a_texcoord'] = (0, 0), (0, +1), (+1, 0), (+1, +1)
program['a_size'] = w,h
program['u_major_grid_width'] = 1.5
program['u_minor_grid_width'] = 1.0
program['u_major_grid_color'] = 0, 0, 0, 1.0
program['u_minor_grid_color'] = 0, 0, 0, 0.5

limits1 = -3.0, +3.0, -1.5, +1.5
limits2 = -np.pi, +np.pi, -np.pi/2, +np.pi/2

major_grid = np.array([1.0, 0.5])*np.pi/(6*1)
minor_grid = np.array([1.0, 0.5])*np.pi/(6*5)
program['u_limits1'] = limits1
program['u_limits2'] = limits2
program['u_antialias'] = 1.0
Z = np.zeros((1,2*1024,4), dtype=np.float32)
program['u_grid'] = Z
program['u_grid'].interpolation = gl.GL_NEAREST

gl.glClearColor(1, 1, 1, 1)
gl.glEnable(gl.GL_BLEND)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

app.run()
