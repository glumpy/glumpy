#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
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

// if edge0 < x <= edge1, return 1.0, otherwise return 0
float segment(float edge0, float edge1, float x)
{
    return step(edge0,x) * (1.0-step(edge1,x));
}


vec3 gray(float t)
{
    return vec3(t);
}

vec3 hot(float t)
{
    return vec3(smoothstep(0.00,0.33,t),
                smoothstep(0.33,0.66,t),
                smoothstep(0.66,1.00,t));
}

vec3 cool(float t)
{
    return mix( vec3(0.0,1.0,1.0), vec3(1.0,0.0,1.0), t);
}

vec3 autumn(float t)
{
    return mix( vec3(1.0,0.0,0.0), vec3(1.0,1.0,0.0), t);
}

vec3 winter(float t)
{
    return mix( vec3(0.0,0.0,1.0), vec3(0.0,1.0,0.5), sqrt(t));
}

vec3 spring(float t)
{
    return mix( vec3(1.0,0.0,1.0), vec3(1.0,1.0,0.0), t);
}

vec3 summer(float t)
{
    return mix( vec3(0.0,0.5,0.4), vec3(1.0,1.0,0.4), t);
}

vec3 ice(float t)
{
   return vec3(t, t, 1.0);
}

vec3 fire(float t)
{
    return mix( mix(vec3(1,1,1), vec3(1,1,0), t),
                mix(vec3(1,1,0), vec3(1,0,0), t*t), t);
}

vec3 ice_and_fire(float t)
{
    return segment(0.0,0.5,t) * ice(2.0*(t-0.0)) +
           segment(0.5,1.0,t) * fire(2.0*(t-0.5));
}

vec3 reds(float t)
{
    return mix(vec3(1,1,1), vec3(1,0,0), t);
}

vec3 greens(float t)
{
    return mix(vec3(1,1,1), vec3(0,1,0), t);
}

vec3 blues(float t)
{
    return mix(vec3(1,1,1), vec3(0,0,1), t);
}

// By Morgan McGuire
vec3 wheel(float t)
{
    return clamp(abs(fract(t + vec3(1.0, 2.0 / 3.0, 1.0 / 3.0)) * 6.0 - 3.0) -1.0, 0.0, 1.0);
}

// By Morgan McGuire
vec3 stripes(float t)
{
    return vec3(mod(floor(t * 64.0), 2.0) * 0.2 + 0.8);
}

// Segmented
vec3 rgb(float t)
{
    return segment(0.00,0.33,t) * vec3(1,0,0)
         + segment(0.33,0.67,t) * vec3(0,1,0)
         + segment(0.67,1.00,t) * vec3(0,0,1);
}



void main(void)
{
    vec2 uv = gl_FragCoord.xy / iResolution.xy;

    float n = 16.0;
    float t = gl_FragCoord.x / iResolution.x;

    // Break up mach bands
    float i = n * gl_FragCoord.y / iResolution.y;

    if (mod(gl_FragCoord.y+n/4., iResolution.y / n) < max(iResolution.y / 100.0, 2.0))
    { gl_FragColor.rgb = vec3(0.0); }
    else if (i > n- 1.0) { gl_FragColor.rgb = gray(uv.x);         }
    else if (i > n- 2.0) { gl_FragColor.rgb = hot(uv.x);          }
    else if (i > n- 3.0) { gl_FragColor.rgb = cool(uv.x);         }
    else if (i > n- 4.0) { gl_FragColor.rgb = autumn(uv.x);       }
    else if (i > n- 5.0) { gl_FragColor.rgb = winter(uv.x);       }
    else if (i > n- 6.0) { gl_FragColor.rgb = spring(uv.x);       }
    else if (i > n- 7.0) { gl_FragColor.rgb = summer(uv.x);       }
    else if (i > n- 8.0) { gl_FragColor.rgb = ice(uv.x);          }
    else if (i > n- 9.0) { gl_FragColor.rgb = fire(uv.x);         }
    else if (i > n-10.0) { gl_FragColor.rgb = ice_and_fire(uv.x); }
    else if (i > n-11.0) { gl_FragColor.rgb = reds(uv.x);         }
    else if (i > n-12.0) { gl_FragColor.rgb = greens(uv.x);       }
    else if (i > n-13.0) { gl_FragColor.rgb = blues(uv.x);        }
    else if (i > n-14.0) { gl_FragColor.rgb = wheel(uv.x);        }
    else if (i > n-15.0) { gl_FragColor.rgb = stripes(uv.x);      }
    else if (i > n-16.0) { gl_FragColor.rgb = rgb(uv.x);          }


    gl_FragColor.a = 1.0;
    // Translate to gamma 2.2 space
    gl_FragColor.rgb = pow(gl_FragColor.rgb, vec3(1.0/2.2));
}
"""


window = app.Window(width=1600, height=800)

@window.event
def on_draw(dt):
    global iGlobalTime
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    program.draw(gl.GL_TRIANGLE_STRIP)

    iGlobalTime += dt
    program["iGlobalTime"] = iGlobalTime
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

iGlobalTime = 0
program = gloo.Program(vertex, fragment, count=4)
program['position'] = [(-1,-1), (-1,+1), (+1,-1), (+1,+1)]
gl.glClearColor(1,1,1,1)
gl.glEnable(gl.GL_BLEND)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
app.run(framerate=60)
