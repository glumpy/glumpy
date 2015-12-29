# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import sys
import math
import numpy as np
from  glumpy import app, gl, glm, gloo, library


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


def find_closest_direct(I, start, end, count):
    Q = (I-start)/(end-start)*count
    mid = ((Q[1:]+Q[:-1]+1)/2).astype(np.int)
    boundary = np.zeros(count, np.int)
    boundary[mid] = 1
    return np.add.accumulate(boundary)

def compute_grid():
    """ Grid reference update """
    n = Z.shape[1]

    epsilon = 1e-10

    xmin, xmax = limits2[:2]
    t1 = major_grid[0]

    start = xmin - math.fmod(xmin, t1)
    if abs(start-xmin) < epsilon: start += t1
    stop  = xmax - math.fmod(xmax, t1)
    if abs(stop-xmax) < epsilon: stop -= t1
    count = (stop-start)/t1+1
    I = np.zeros(count+2)
    I[0], I[-1] = xmin, xmax
    I[1:-1] = np.linspace(start, stop, count, endpoint=True)
    Z[..., 0] = I[find_closest_direct(I, start=xmin, end=xmax, count=n)]

    t2 = minor_grid[0]
    start = xmin - math.fmod(xmin, t2)
    if abs(start-xmin) < epsilon: start += t2
    stop  = xmax - math.fmod(xmax, t2)
    if abs(stop-xmax) < epsilon: stop -= t2
    count = (stop-start)/t2+1
    I = np.zeros(count+2)
    I[0], I[-1] = xmin, xmax
    I[1:-1] = np.linspace(start, stop, count, endpoint=True)
    Z[..., 1] = I[find_closest_direct(I, start=xmin, end=xmax, count=n)]

    ymin, ymax = limits2[2:]

    t1 = major_grid[1]
    start = ymin - math.fmod(ymin, t1)
    if abs(start-ymin) < epsilon: start += t1
    stop  = ymax - math.fmod(ymax, t1)
    if abs(stop-ymax) < epsilon: stop -= t1
    count = (stop-start)/t1+1
    I = np.zeros(count+2)
    I[0], I[-1] = ymin, ymax
    I[1:-1] = np.linspace(start, stop, count, endpoint=True)
    Z[..., 2] = I[find_closest_direct(I, start=ymin, end=ymax, count=n)]

    t2 = minor_grid[1]
    start = ymin - math.fmod(ymin, t2)
    if abs(start-ymin) < epsilon: start += t2
    stop  = ymax - math.fmod(ymax, t2)
    if abs(stop-ymax) < epsilon: stop -= t2
    count = (stop-start)/t2+1
    I = np.zeros(count+2)
    I[0], I[-1] = ymin, ymax
    I[1:-1] = np.linspace(start, stop, count, endpoint=True)
    Z[..., 3] = I[find_closest_direct(I, start=ymin, end=ymax, count=n)]



rows,cols = 4,4
window = app.Window(width=1024, height=1024, color=(1,1,1,1))


@window.event
def on_draw(dt):
    window.clear()
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
indices[:,:] += 4*np.arange(rows*cols,dtype=np.uint32).reshape(rows,cols,1)
indices = indices.ravel()
indices = indices.view(gloo.IndexBuffer)


program = gloo.Program(vertex, library.get("misc/irregular-grid.frag"))
program.bind(vertices)

program["rows"] = rows
program["cols"] = cols
program['u_major_grid_width'] = 1.5
program['u_minor_grid_width'] = 1.0
program['u_major_grid_color'] = 0, 0, 0, 1.0
program['u_minor_grid_color'] = 0, 0, 0, 0.5

# Polar projection example
if 1:
    limits1 = -5.1, +5.1, -5.1, +5.1
    limits2 = 1.0, 5.0, 0.0, 2*np.pi
    major_grid = np.array([ 1.00, np.pi/6])
    minor_grid = np.array([ 0.25, np.pi/60])

# Cartesian projection limits
if 0:
    limits1 = -5.1, +5.1, -5.1, +5.1
    limits2 = -5, +5, -5, +5
    major_grid = np.array([ 1.0, 1.0])
    minor_grid = np.array([ 0.2, 0.2])

program['u_limits1'] = limits1
program['u_limits2'] = limits2
program['u_antialias'] = 1.0
Z = np.zeros((1,2*1024,4), dtype=np.float32)
program['u_grid'] = Z
program['u_grid'].interpolation = gl.GL_NEAREST

app.run()
