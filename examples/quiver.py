# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gl, glm, gloo

vertex = """
    attribute vec2 position;
    void main()
    {
        gl_Position = vec4(position, 0.0, 1.0);
    }
"""

fragment = """
#include "math/constants.glsl"
#include "arrows/arrows.glsl"
#include "antialias/antialias.glsl"

uniform vec2 iResolution;
uniform vec2 iMouse;
void main()
{
    const float M_PI = 3.14159265358979323846;
    const float SQRT_2 = 1.4142135623730951;
    const float linewidth = 3.0;
    const float antialias =  1.0;

    const float rows = 32.0;
    const float cols = 32.0;
    float body = min(iResolution.x/cols, iResolution.y/rows) / SQRT_2;
    vec2 texcoord = gl_FragCoord.xy;
    vec2 size   = iResolution.xy / vec2(cols,rows);
    vec2 center = (floor(texcoord/size) + vec2(0.5,0.5)) * size;



    texcoord -= center;

    // float theta = M_PI/3.0 + 0.1*(center.x / cols + center.y / rows);
    float theta = M_PI-atan(center.y-iMouse.y,  center.x-iMouse.x);

    float cos_theta = cos(theta);
    float sin_theta = sin(theta);
    texcoord = vec2(cos_theta*texcoord.x - sin_theta*texcoord.y,
                    sin_theta*texcoord.x + cos_theta*texcoord.y);

    // float d = arrow_curved(texcoord, body, 0.25*body, linewidth, antialias);
    float d = arrow_stealth(texcoord, body, 0.25*body, linewidth, antialias);
    // float d = arrow_triangle_90(texcoord, body, 0.15*body, linewidth, antialias);
    // float d = arrow_triangle_60(texcoord, body, 0.20*body, linewidth, antialias);
    // float d = arrow_triangle_30(texcoord, body, 0.25*body, linewidth, antialias);
    // float d = arrow_angle_90(texcoord, body, 0.15*body, linewidth, antialias);
    // float d = arrow_angle_60(texcoord, body, 0.20*body, linewidth, antialias);
    // float d = arrow_angle_30(texcoord, body, 0.25*body, linewidth, antialias);

    gl_FragColor = filled(d, linewidth, antialias, vec4(0,0,0,1));
    // gl_FragColor = stroke(d, linewidth, antialias, vec4(0,0,0,1));
}
"""


window = app.Window(width=2*512, height=2*512, color=(1,1,1,1))

@window.event
def on_draw(dt):
    window.clear()
    program.draw(gl.GL_TRIANGLE_STRIP)

@window.event
def on_resize(width, height):
    program["iResolution"] = width, height

@window.event
def on_mouse_motion(x, y, dx, dy):
    program["iMouse"] = x,window.height-y

program = gloo.Program(vertex, fragment, count=4)
dx,dy = 1,1
program['position'] = (-dx,-dy), (-dx,+dy), (+dx,-dy), (+dx,+dy)

app.run()
