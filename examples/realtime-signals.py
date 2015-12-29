# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
# Realtime signals example
#
# Implementation uses a ring buffer such that only new values are uploaded in
# GPU memory. This requires the corresponding numpy array to have a
# Fortran-like layout.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gloo, gl

vertex = """
uniform int index, size, count;
attribute float x_index, y_index, y_value;
varying float do_discard;
void main (void)
{
    float x = 2*(mod(x_index - index, size) / (size)) - 1.0;
    if ((x >= +1.0) || (x <= -1.0)) do_discard = 1;
    else                            do_discard = 0;
    float y = (2*((y_index+.5)/(count))-1) + y_value;
    gl_Position = vec4(x, y, 0, 1);
}
"""

fragment = """
varying float do_discard;
void main(void)
{
    if (do_discard > 0) discard;
    gl_FragColor = vec4(0,0,0,1);
}
"""

window = app.Window(width=1500, height=1000, color=(1,1,1,1))

@window.event
def on_draw(dt):
    global size, count
    window.clear()
    program.draw(gl.GL_LINES, I)
    index = int(program["index"])
    y = program["y_value"].reshape(size,count)

    yscale = 1.0/count
    y[index] = yscale * np.random.uniform(-1,+1,count)
    program["index"] = (index + 1) % size

count, size = 64, 1000
program = gloo.Program(vertex, fragment, count=size*count)
program["size"] = size
program["count"] = count
program["x_index"] = np.repeat(np.arange(size),count)
program["y_index"] = np.tile(np.arange(count),size)
program["y_value"] = 0

# Compute indices
I = np.repeat(np.arange(size+1,dtype=np.uint32)*count,2)[1:-1]
I[-1] = I[0]
I = np.tile(I,count).reshape(count,2*size)
I += np.repeat(np.arange(count,dtype=np.uint32),2*size).reshape(count,2*size)
I = I.view(gloo.IndexBuffer)

app.run()
