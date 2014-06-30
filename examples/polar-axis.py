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

vertex   = "./polar.vert"
fragment = "./polar.frag"



def find_closest_direct(I, start, end, count):
    Q = (I-start)/(end-start)*count
    mid = ((Q[1:]+Q[:-1]+1)/2).astype(np.int)
    boundary = np.zeros(count, np.int)
    boundary[mid] = 1
    return np.add.accumulate(boundary)

def update_grid():

    n = Z.shape[1]

    ymin, ymax = ylim
    t1 = major_grid[0]
    t2 = minor_grid[0]

    I1 = np.linspace(ymin, ymax, (ymax-ymin)/t1+1, endpoint=True)
    Z[..., 0] = I1[find_closest_direct(I1, start=ymin, end=ymax, count=n)]

    I2 = np.linspace(ymin, ymax, (ymax-ymin)/t2+1, endpoint=True)
    Z[..., 1] = I2[find_closest_direct(I2, start=ymin, end=ymax, count=n)]

    xmin, xmax = 0,360
    t1 = major_grid[1]*1
    t2 = minor_grid[1]*1

    I3 = np.linspace(xmin, xmax, (xmax-xmin)/t1, endpoint=False)
    Z[..., 2] = I3[find_closest_direct(I3, start=xmin, end=xmax, count=n)]

    I4 = np.linspace(xmin, xmax, (xmax-xmin)/t2, endpoint=False)
    Z[..., 3] = I4[find_closest_direct(I4, start=xmin, end=xmax, count=n)]

    program['u_grid'][...] = Z



window = app.Window(width=1024, height=1024)

@window.event
def on_draw():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    program.draw(gl.GL_TRIANGLE_STRIP)


@window.event
def on_resize(width, height):
    gl.glViewport(0, 0, width, height)
    projection = glm.ortho(0, width, 0, height, -1, +1)
    program['u_projection'] = projection
    update_grid()

@window.event
def on_mouse_drag(x, y, dx, dy, button):
    global translate, scale
    _, _, w, h = gl.glGetIntegerv(gl.GL_VIEWPORT)
    translate = [translate[0] + dx, translate[1] - dy]
    program['u_translate'] = translate
    update_grid()


@window.event
def on_mouse_scroll(x, y, dx, dy):
    global translate, scale
    _, _, w, h = gl.glGetIntegerv(gl.GL_VIEWPORT)
    y = h-y

    x -= 1024/2
    y -= 1024/2

    s = min(max(0.25, scale + .01 * dy * scale), 200)
    translate[0] = x - s * (x - translate[0]) / scale
    translate[1] = y - s * (y - translate[1]) / scale
    translate = [translate[0], translate[1]]
    scale = s
    program['u_translate'] = translate
    program['u_scale'] = scale
    update_grid()


program = gloo.Program(vertex, fragment, 4)
program['u_model']      = np.eye(4)
program['u_view']       = np.eye(4)
program['u_projection'] = np.eye(4)

w,h = 1024,1024
program['a_position'] = (0, 0), (0, h), (w, 0), (w, h)
program['a_texcoord'] = (-1, -1), (-1, +1), (+1, -1), (+1, +1)
program['u_major_grid_width'] = 1.5
program['u_minor_grid_width'] = 1.0
program['u_major_grid_color'] = 0, 0, 0, 1.0
program['u_minor_grid_color'] = 0, 0, 0, 0.5

scale = 1
translate = [0,0]
xlim = 0*np.pi/180.0, 330*np.pi/180.0
ylim = 1,3

major_grid = np.array([1.00,  30.0])
minor_grid = np.array([0.10,   3.0])

program['u_xlim'] = xlim
program['u_ylim'] = ylim
program['u_scale'] = scale
program['u_translate'] = translate


program['u_antialias'] = 1.0
Z = np.zeros((1, 2 * 1024, 4), dtype=np.float32)
program['u_grid'] = Z
program['u_grid'].interpolation = gl.GL_NEAREST


gl.glClearColor(1, 1, 1, 1)
gl.glEnable(gl.GL_BLEND)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

app.run()
