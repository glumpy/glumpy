#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import sys
import numpy as np
from  glumpy import app, gl, glm, gloo


vertex = """
const float gap = 4.0;

uniform mat4 projection;
uniform vec4 viewport;
uniform float rows, cols;

attribute float row, col;
attribute vec2 texcoord;

varying vec2 v_texcoord;
varying vec2 v_size;

void main (void)
{
    v_size = viewport.zw / vec2(cols, rows);

    if (v_size.x > v_size.y)
        v_texcoord = texcoord * vec2(v_size.x/v_size.y,1.0);
    else
        v_texcoord = texcoord * vec2(1.0, v_size.y/v_size.x);

    vec2 position = vec2(gap)/2.0
                  + vec2(col,row)*v_size
                  + (texcoord + 0.5) * (v_size - vec2(gap));
    gl_Position = projection * vec4(position, 0.0, 1.0);
}
"""

rows,cols = 2,2
window = app.Window(width=1024, height=1024)


def find_closest_direct(I, start, end, count):
    Q = (I-start)/(end-start)*count
    mid = ((Q[1:]+Q[:-1]+1)/2).astype(np.int)
    boundary = np.zeros(count, np.int)
    boundary[mid] = 1
    return np.add.accumulate(boundary)

def compute_grid():
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


@window.event
def on_draw():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    program.draw(gl.GL_TRIANGLES, indices)

@window.event
def on_resize(width, height):
    program['projection'] = glm.ortho(0, width, 0, height, -1, +1)
    program['viewport'] = 0,0,width,height
    compute_grid()
    program['u_grid'][...] = Z



vertices = np.zeros((rows,cols,4), dtype=[("row",      np.float32, 1),
                                          ("col",      np.float32, 1),
                                          ("texcoord", np.float32, 2)])
vertices = vertices.view(gloo.VertexBuffer)

C,R = np.meshgrid(np.arange(cols),np.arange(rows))
vertices[:,:]["texcoord"] = (-0.5,-0.5), (-0.5,+0.5), (+0.5,+0.5), (+0.5,-0.5)
vertices[:,:]["row"]      = R.reshape(rows,cols,1)
vertices[:,:]["col"]      = C.reshape(rows,cols,1)

indices = np.zeros( (rows,cols, 6), dtype=np.uint32 )
indices[:,:] = 0,1,2,0,2,3
indices[:,:] += 4*np.arange(rows*cols).reshape(rows,cols,1)
indices = indices.ravel()
indices = indices.view(gloo.IndexBuffer)


program = gloo.Program(vertex, "grid.frag")
program.bind(vertices)

program["rows"] = rows
program["cols"] = cols
program['u_major_grid_width'] = 1.5
program['u_minor_grid_width'] = 1.0
program['u_major_grid_color'] = 0, 0, 0, 1.0
program['u_minor_grid_color'] = 0, 0, 0, 0.5

limits1 = -5, +5, -5, +5
limits2 = 1, 5, 0, 2*np.pi

major_grid = np.array([ 1.0, np.pi/6])
minor_grid = np.array([ 0.2, np.pi/60])

program['u_limits1'] = limits1
program['u_limits2'] = limits2
program['u_antialias'] = 1.0
Z = np.zeros((1,2*1024,4), dtype=np.float32)
program['u_grid'] = Z
program['u_grid'].interpolation = gl.GL_NEAREST


gl.glClearColor(1.0, 1.0, 1.0, 1.0)
gl.glDisable(gl.GL_DEPTH_TEST)
gl.glEnable(gl.GL_BLEND)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
app.run()
