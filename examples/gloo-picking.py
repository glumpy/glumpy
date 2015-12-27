# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gl, gloo, glm
from glumpy.transforms import Trackball

vertex = """
#include "math/constants.glsl"

uniform float linewidth;
uniform float antialias;

attribute vec4  fg_color;
attribute vec4  bg_color;
attribute float size;
attribute vec3  position;
attribute float id;

varying vec4  v_id;
varying float v_size;
varying vec4  v_fg_color;
varying vec4  v_bg_color;
void main (void)
{
    // id to vec3 (alpha must be one or color will be blended
    v_id = vec4 ( mod(floor(id / (256*256)), 256) / 255.0,
                  mod(floor(id /     (256)), 256) / 255.0,
                  mod(floor(id /       (1)), 256) / 255.0,
                  1.0 );
    v_size = size;
    v_fg_color = fg_color;
    v_bg_color = bg_color;
    gl_Position = <transform(vec4(position,1.0))>;
    gl_PointSize = M_SQRT2 * size + 2.0 * (linewidth + 1.5*antialias);
}
"""

fragment = """
#include "markers/disc.glsl"
#include "math/constants.glsl"
#include "antialias/antialias.glsl"

uniform float linewidth;
uniform float antialias;

varying vec4  v_id;
varying float v_size;
varying vec4  v_fg_color;
varying vec4  v_bg_color;

void main()
{
    vec2 P = gl_PointCoord.xy - vec2(0.5,0.5);
    float point_size = M_SQRT2*v_size  + 2 * (linewidth + 1.5*antialias);
    float distance = marker_disc(P*point_size, v_size);
    vec4 color = outline(distance, linewidth, antialias, v_fg_color, v_bg_color);
    gl_FragData[0] = color;
    gl_FragData[1] = v_id;
}
"""

quad_vertex = """
attribute vec2 position;
varying vec2 v_texcoord;
void main(void)
{
    gl_Position = vec4(position,0,1);
    v_texcoord = (position+1.0)/2.0;
}"""

quad_fragment = """
uniform sampler2D color;
varying vec2 v_texcoord;
void main(void)
{
    gl_FragColor = texture2D(color,v_texcoord);
}
"""

window = app.Window(width=1000, height=1000, color=(1,1,1,1))

n = 5000
program = gloo.Program(vertex, fragment, count=n)
program['position'] = 0.75 * np.random.randn(n,3)
program['size']     = np.random.uniform(20,30,n)
program['fg_color'] = 0,0,0,1
program['bg_color'] = np.random.uniform(0.75, 1.00, (n, 4))
program['bg_color'][:,3] = 1
program['linewidth'] = 1.0
program['antialias'] = 1.0
program['transform'] = Trackball()
program["id"] = np.arange(n,dtype=np.float32)

quad = gloo.Program(quad_vertex, quad_fragment, count=4)
quad['position']= [(-1,-1), (-1,1), (1,-1), (1,1)]

color = np.zeros((window.height,window.width,4),np.ubyte).view(gloo.Texture2D)
color.interpolation = gl.GL_LINEAR
pick = np.zeros((window.height,window.width,4),np.ubyte).view(gloo.Texture2D)
pick.interpolation = gl.GL_LINEAR
framebuffer = gloo.FrameBuffer(color=[color,pick])
quad["color"] = color

index = 0
mouse = 0,0

@window.event
def on_draw(dt):
    gl.glEnable(gl.GL_DEPTH_TEST)

    framebuffer.activate()
    window.clear()
    program.draw(gl.GL_POINTS)
    if mouse is not None:
        gl.glReadBuffer(gl.GL_COLOR_ATTACHMENT1, gl.GL_FRONT)
        r,g,b,a = gl.glReadPixels(mouse[0],mouse[1],1,1, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE)
        if type(r) is not int: r = ord(r)
        if type(g) is not int: g = ord(g)
        if type(b) is not int: b = ord(b)
        index = b + 256*g + 256*256*r
        if index < len(program):
            program["bg_color"][index] = 0,0,0,1
    framebuffer.deactivate()
    gl.glDisable(gl.GL_DEPTH_TEST)
    quad.draw(gl.GL_TRIANGLE_STRIP)

@window.event
def on_resize(width, height):
    framebuffer.resize(width,height)
    quad["color"] = framebuffer.color[0]

@window.event
def on_mouse_motion(x,y, dx, dy):
    global mouse
    mouse = int(x), window.height-int(y)

window.attach(program['transform'])
app.run()
