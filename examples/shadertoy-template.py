# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
""" Shadertoy template to test a shadertoy from www.shadertoy.com """

import datetime
import numpy as np
from glumpy import app, gl, gloo

vertex = """
attribute vec2 position;
void main (void)
{
    gl_Position = vec4(position, 0.0, 1.0);
}
"""

fragment = """
uniform vec3      iResolution; // Viewport resolution (in pixels)
uniform float     iGlobalTime; // Shader playback time (in seconds)
uniform vec4      iMouse;      // Mouse pixel coords. xy: current (if MLB down) + zw: click
uniform vec4      iDate;       // Date as (year, month, day, time in seconds)
// uniform float     iChannelTime[4];       // Channel playback time (in seconds)
// uniform vec3      iChannelResolution[4]; // Channel resolution (in pixels)
// uniform sampler2D iChannel[4];           // Input channel. (XX = 2D or Cube)

// Put your shadertoy code here
void main(void)
{
    vec2 uv = gl_FragCoord.xy / iResolution.xy;
    gl_FragColor = vec4(uv,0.5*sin(1.0+iGlobalTime),1.0);
}
"""


window = app.Window(width=800, height=800)

@window.event
def on_draw(dt):
    window.clear()
    program.draw(gl.GL_TRIANGLE_STRIP)
    program["iGlobalTime"] += dt
    today = datetime.datetime.now()
    seconds = (today.hour*60*60 + today.minute*60 + today.second)
    program["iDate"] = today.year, today.month, today.day, seconds

@window.event
def on_resize(width, height):
    program["iResolution"] = width, height, 0

@window.event
def on_mouse_drag(x, y, dx, dy, button):
    buttons = {app.window.mouse.NONE   : 0, app.window.mouse.LEFT  : 1,
               app.window.mouse.MIDDLE : 2, app.window.mouse.RIGHT : 3 }
    program["iMouse"] = x, y, buttons[button], 0

program = gloo.Program(vertex, fragment, count=4)
program['position'] = [(-1,-1), (-1,+1), (+1,-1), (+1,+1)]
program["iGlobalTime"] = 0
gl.glEnable(gl.GL_BLEND)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
app.run(framerate=60)
