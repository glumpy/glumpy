# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
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
    if( pingpong == 0 )
        v = texture2D(texture, v_texcoord).r;
    else
        v = texture2D(texture, v_texcoord).b;
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
uniform sampler2D texture; // U,V:= r,g, other channels ignored
uniform sampler2D params;  // rU,rV,f,k := r,g,b,a
uniform float dx;          // horizontal distance between texels
uniform float dy;          // vertical distance between texels
uniform float dd;          // unit of distance
uniform float dt;          // unit of time
varying vec2 v_texcoord;
void main(void)
{
    float center = -(4.0+4.0/sqrt(2.0));  // -1 * other weights
    float diag   = 1.0/sqrt(2.0);         // weight for diagonals
    vec2 p = v_texcoord;                  // center coordinates

    vec2 c,l;
    if( pingpong == 0 ) {
        c = texture2D(texture, p).rg;    // central value
        // Compute Laplacian
        l = ( texture2D(texture, p + vec2(-dx,-dy)).rg
            + texture2D(texture, p + vec2( dx,-dy)).rg
            + texture2D(texture, p + vec2(-dx, dy)).rg
            + texture2D(texture, p + vec2( dx, dy)).rg) * diag
            + texture2D(texture, p + vec2(-dx, 0.0)).rg
            + texture2D(texture, p + vec2( dx, 0.0)).rg
            + texture2D(texture, p + vec2(0.0,-dy)).rg
            + texture2D(texture, p + vec2(0.0, dy)).rg
            + c * center;
    } else {
        c = texture2D(texture, p).ba;    // central value
        // Compute Laplacian
        l = ( texture2D(texture, p + vec2(-dx,-dy)).ba
            + texture2D(texture, p + vec2( dx,-dy)).ba
            + texture2D(texture, p + vec2(-dx, dy)).ba
            + texture2D(texture, p + vec2( dx, dy)).ba) * diag
            + texture2D(texture, p + vec2(-dx, 0.0)).ba
            + texture2D(texture, p + vec2( dx, 0.0)).ba
            + texture2D(texture, p + vec2(0.0,-dy)).ba
            + texture2D(texture, p + vec2(0.0, dy)).ba
            + c * center;
    }

    float u = c.r;           // compute some temporary
    float v = c.g;           // values which might save
    float lu = l.r;          // a few GPU cycles
    float lv = l.g;
    float uvv = u * v * v;

    vec4 q = texture2D(params, p).rgba;
    float ru = q.r;          // rate of diffusion of U
    float rv = q.g;          // rate of diffusion of V
    float f  = q.b;          // some coupling parameter
    float k  = q.a;          // another coupling parameter

    float du = ru * lu / dd - uvv + f * (1.0 - u); // Gray-Scott equation
    float dv = rv * lv / dd + uvv - (f + k) * v;   // diffusion+-reaction

    u += du * dt;
    v += dv * dt;

    if( pingpong == 1 ) {
        gl_FragColor = vec4(clamp(u, 0.0, 1.0), clamp(v, 0.0, 1.0), c);
    } else {
        gl_FragColor = vec4(c, clamp(u, 0.0, 1.0), clamp(v, 0.0, 1.0));
    }
}
"""


window = app.Window(width=1024, height=1024)
cwidth,cheight = 256, 256

@window.event
def on_draw(dt):
    global pingpong

    pingpong = 1 - pingpong
    compute["pingpong"] = pingpong
    render["pingpong"] = pingpong

    gl.glDisable(gl.GL_BLEND)

    framebuffer.activate()
    gl.glViewport(0, 0, cwidth, cheight)
    compute.draw(gl.GL_TRIANGLE_STRIP)
    framebuffer.deactivate()

    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    gl.glViewport(0, 0, window.width, window.height)
    render.draw(gl.GL_TRIANGLE_STRIP)


dt = 1.0
dd = 1.5
w,h = cwidth, cheight
species = {
    # name : [r_u, r_v, f, k]
    'Bacteria 1': [0.16, 0.08, 0.035, 0.065],
    'Bacteria 2': [0.14, 0.06, 0.035, 0.065],
    'Coral': [0.16, 0.08, 0.060, 0.062],
    'Fingerprint': [0.19, 0.05, 0.060, 0.062],
    'Spirals': [0.10, 0.10, 0.018, 0.050],
    'Spirals Dense': [0.12, 0.08, 0.020, 0.050],
    'Spirals Fast': [0.10, 0.16, 0.020, 0.050],
    'Unstable': [0.16, 0.08, 0.020, 0.055],
    'Worms 1': [0.16, 0.08, 0.050, 0.065],
    'Worms 2': [0.16, 0.08, 0.054, 0.063],
    'Zebrafish': [0.16, 0.08, 0.035, 0.060] }
P = np.zeros((h, w, 4), dtype=np.float32)
P[:, :] = species['Unstable']

P[:, :] = species['Coral']

UV = np.zeros((h, w, 4), dtype=np.float32)
UV[:, :, 0] = 1.0
r = 32
UV[h/2-r:h/2+r,w/2-r:w/2+r,0] = 0.50
UV[h/2-r:h/2+r,w/2-r:w/2+r,1] = 0.25
UV += np.random.uniform(0.00, 0.01, (h, w, 4))
UV[:,:,2] = UV[:,:,0]
UV[:,:,3] = UV[:,:,1]

pingpong = 1
compute = gloo.Program(compute_vertex, compute_fragment, count=4)
compute["params"] = P
compute["texture"] = UV
compute["texture"].interpolation = gl.GL_NEAREST
compute["texture"].wrapping = gl.GL_CLAMP_TO_EDGE
compute["position"] = [(-1, -1), (-1, +1), (+1, -1), (+1, +1)]
compute["texcoord"] = [(0, 0), (0, 1), (1, 0), (1, 1)]
compute['dt'] = dt
compute['dx'] = 1.0 / w
compute['dy'] = 1.0 / h
compute['dd'] = dd
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
