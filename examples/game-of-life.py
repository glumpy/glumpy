# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
# Author:   Nicolas P .Rougier
# Date:     06/03/2014
# Abstract: GPU computing using the framebuffer
# Keywords: framebuffer, GPU computing, cellular automata
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gl, glm, gloo


render_vertex = """
attribute vec2 position;
attribute vec2 texcoord;
varying vec2 v_texcoord;
void main()
{
    gl_Position = vec4(position, 0.0, 1.0);
    v_texcoord = texcoord;
}
"""

render_fragment = """
uniform int pingpong;
uniform sampler2D texture;
varying vec2 v_texcoord;
void main()
{
    float v;
    v = texture2D(texture, v_texcoord)[pingpong];
    gl_FragColor = vec4(1.0-v, 1.0-v, 1.0-v, 1.0);
}
"""

compute_vertex = """
attribute vec2 position;
attribute vec2 texcoord;
varying vec2 v_texcoord;
void main()
{
    gl_Position = vec4(position, 0.0, 1.0);
    v_texcoord = texcoord;
}
"""

compute_fragment = """
uniform int pingpong;
uniform sampler2D texture;
uniform float dx;          // horizontal distance between texels
uniform float dy;          // vertical distance between texels
varying vec2 v_texcoord;
void main(void)
{
    vec2  p = v_texcoord;
    float old_state, new_state, count;

    old_state = texture2D(texture, p)[pingpong];
    count = texture2D(texture, p + vec2(-dx,-dy))[pingpong]
            + texture2D(texture, p + vec2( dx,-dy))[pingpong]
            + texture2D(texture, p + vec2(-dx, dy))[pingpong]
            + texture2D(texture, p + vec2( dx, dy))[pingpong]
            + texture2D(texture, p + vec2(-dx, 0.0))[pingpong]
            + texture2D(texture, p + vec2( dx, 0.0))[pingpong]
            + texture2D(texture, p + vec2(0.0,-dy))[pingpong]
            + texture2D(texture, p + vec2(0.0, dy))[pingpong];

    new_state = old_state;
    if( old_state > 0.5 ) {
        // Any live cell with fewer than two live neighbours dies
        // as if caused by under-population.
        if( count  < 1.5 )
            new_state = 0.0;

        // Any live cell with two or three live neighbours
        // lives on to the next generation.

        // Any live cell with more than three live neighbours dies,
        //  as if by overcrowding.
        else if( count > 3.5 )
            new_state = 0.0;
    } else {
        // Any dead cell with exactly three live neighbours becomes
        //  a live cell, as if by reproduction.
       if( (count > 2.5) && (count < 3.5) )
           new_state = 1.0;
    }
    if( pingpong == 0 ) {
        gl_FragColor[1] = new_state;
        gl_FragColor[0] = old_state;
    } else {
        gl_FragColor[0] = new_state;
        gl_FragColor[1] = old_state;
    }
}
"""


window = app.Window(width=512, height=512)

@window.event
def on_draw(dt):
    global pingpong

    width,height = 512,512

    pingpong = 1 - pingpong
    compute["pingpong"] = pingpong
    render["pingpong"] = pingpong

    gl.glDisable(gl.GL_BLEND)

    framebuffer.activate()
    gl.glViewport(0, 0, width, height)
    compute.draw(gl.GL_TRIANGLE_STRIP)
    framebuffer.deactivate()

    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    gl.glViewport(0, 0, width, height)
    render.draw(gl.GL_TRIANGLE_STRIP)


w, h = 512,512
Z = np.zeros((h, w, 4), dtype=np.float32)
Z[...] = np.random.randint(0, 2, (h, w, 4))
Z[:256, :256, :] = 0
gun = """
........................O...........
......................O.O...........
............OO......OO............OO
...........O...O....OO............OO
OO........O.....O...OO..............
OO........O...O.OO....O.O...........
..........O.....O.......O...........
...........O...O....................
............OO......................"""
x, y = 0, 0
for i in range(len(gun)):
    if gun[i] == '\n':
        y += 1
        x = 0
    elif gun[i] == 'O':
        Z[y, x] = 1
    x += 1

pingpong = 1
compute = gloo.Program(compute_vertex, compute_fragment, count=4)
compute["texture"] = Z
compute["texture"].interpolation = gl.GL_NEAREST
compute["texture"].wrapping = gl.GL_CLAMP_TO_EDGE
compute["position"] = [(-1, -1), (-1, +1), (+1, -1), (+1, +1)]
compute["texcoord"] = [(0, 0), (0, 1), (1, 0), (1, 1)]
compute['dx'] = 1.0 / w
compute['dy'] = 1.0 / h
compute['pingpong'] = pingpong


render = gloo.Program(render_vertex, render_fragment, count=4)
render["position"] = [(-1, -1), (-1, +1), (+1, -1), (+1, +1)]
render["texcoord"] = [(0, 0), (0, 1), (1, 0), (1, 1)]
render["texture"] = compute["texture"]
render["texture"].interpolation = gl.GL_LINEAR
render["texture"].wrapping = gl.GL_CLAMP_TO_EDGE
render['pingpong'] = pingpong

framebuffer = gloo.FrameBuffer(color=compute["texture"],
                               depth=gloo.DepthBuffer(w, h))
app.run(framerate=0)
