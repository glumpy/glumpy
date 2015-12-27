# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
""" This example shows colormap functions (faster than 1d texture lookup) """

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



// if edge0 < x <= edge1, return 1.0, otherwise return 0
float segment(float edge0, float edge1, float x)
{
    return step(edge0,x) * (1.0-step(edge1,x));
}

// return under if t < 0, over if t > 1, color else
vec3 underover(float t, vec3 color, vec3 under, vec3 over)
{
    return step(t,0.0)*under + segment(0.0,1.0,t)*color + step(1.0,t)*over;
}


vec3 gray(float t)
{
    return vec3(t);
}
vec3 gray(float t, vec3 under, vec3 over)
{
    return underover(t, gray(t), under, over);
}


vec3 hot(float t)
{
    return vec3(smoothstep(0.00,0.33,t),
                smoothstep(0.33,0.66,t),
                smoothstep(0.66,1.00,t));
}
vec3 hot(float t, vec3 under, vec3 over)
{
    return underover(t, hot(t), under, over);
}


vec3 cool(float t)
{
    return mix( vec3(0.0,1.0,1.0), vec3(1.0,0.0,1.0), t);
}
vec3 cool(float t, vec3 under, vec3 over)
{
    return underover(t, cool(t), under, over);
}


vec3 autumn(float t)
{
    return mix( vec3(1.0,0.0,0.0), vec3(1.0,1.0,0.0), t);
}
vec3 autumn(float t, vec3 under, vec3 over)
{
    return underover(t, autumn(t), under, over);
}


vec3 winter(float t)
{
    return mix( vec3(0.0,0.0,1.0), vec3(0.0,1.0,0.5), sqrt(t));
}
vec3 winter(float t, vec3 under, vec3 over)
{
    return underover(t, winter(t), under, over);
}


vec3 spring(float t)
{
    return mix( vec3(1.0,0.0,1.0), vec3(1.0,1.0,0.0), t);
}
vec3 spring(float t, vec3 under, vec3 over)
{
    return underover(t, spring(t), under, over);
}


vec3 summer(float t)
{
    return mix( vec3(0.0,0.5,0.4), vec3(1.0,1.0,0.4), t);
}
vec3 summer(float t, vec3 under, vec3 over)
{
    return underover(t, summer(t), under, over);
}


vec3 ice(float t)
{
   return vec3(t, t, 1.0);
}
vec3 ice(float t, vec3 under, vec3 over)
{
    return underover(t, ice(t), under, over);
}


vec3 fire(float t)
{
    return mix( mix(vec3(1,1,1), vec3(1,1,0), t),
                mix(vec3(1,1,0), vec3(1,0,0), t*t), t);
}
vec3 fire(float t, vec3 under, vec3 over)
{
    return underover(t, fire(t), under, over);
}

vec3 ice_and_fire(float t)
{
    return segment(0.0,0.5,t) * ice(2.0*(t-0.0)) +
           segment(0.5,1.0,t) * fire(2.0*(t-0.5));
}
vec3 ice_and_fire(float t, vec3 under, vec3 over)
{
    return underover(t, ice_and_fire(t), under, over);
}

vec3 reds(float t)
{
    return mix(vec3(1,1,1), vec3(1,0,0), t);
}
vec3 reds(float t, vec3 under, vec3 over)
{
    return underover(t, reds(t), under, over);
}

vec3 greens(float t)
{
    return mix(vec3(1,1,1), vec3(0,1,0), t);
}
vec3 greens(float t, vec3 under, vec3 over)
{
    return underover(t, greens(t), under, over);
}

vec3 blues(float t)
{
    return mix(vec3(1,1,1), vec3(0,0,1), t);
}
vec3 blues(float t, vec3 under, vec3 over)
{
    return underover(t, blues(t), under, over);
}


// By Morgan McGuire
vec3 wheel(float t)
{
    return clamp(abs(fract(t + vec3(1.0, 2.0 / 3.0, 1.0 / 3.0)) * 6.0 - 3.0) -1.0, 0.0, 1.0);
}
vec3 wheel(float t, vec3 under, vec3 over)
{
    return underover(t, wheel(t), under, over);
}

// By Morgan McGuire
vec3 stripes(float t)
{
    return vec3(mod(floor(t * 64.0), 2.0) * 0.2 + 0.8);
}
vec3 stripes(float t, vec3 under, vec3 over)
{
    return underover(t, stripes(t), under, over);
}

// Discrete
vec3 discrete(float t)
{
    return segment(0.0,0.2,t) * vec3(1,0,0)
         + segment(0.2,0.5,t) * vec3(0,1,0)
         + segment(0.5,1.0,t) * vec3(0,0,1);
}
vec3 discrete(float t, vec3 under, vec3 over)
{
    return underover(t, discrete(t), under, over);
}


void main(void)
{
    const float n = 17.0;

    vec2 uv = gl_FragCoord.xy / iResolution.xy;
    float t = gl_FragCoord.x / iResolution.x;

    // Discretization level
    // float levels = 32.0;
    // t = floor(t*levels)/levels;

    // Break up mach bands
    float i = n * gl_FragCoord.y / iResolution.y;

    if (mod(gl_FragCoord.y+n/4., iResolution.y / n) < max(iResolution.y / 200.0, 1.0))
    { gl_FragColor.rgb = vec3(0.0); }
    else if (i > n- 1.0) { gl_FragColor.rgb = gray(t);         }
    else if (i > n- 2.0) { gl_FragColor.rgb = hot(t);          }
    else if (i > n- 3.0) { gl_FragColor.rgb = cool(t);         }
    else if (i > n- 4.0) { gl_FragColor.rgb = autumn(t);       }
    else if (i > n- 5.0) { gl_FragColor.rgb = winter(t);       }
    else if (i > n- 6.0) { gl_FragColor.rgb = spring(t);       }
    else if (i > n- 7.0) { gl_FragColor.rgb = summer(t);       }
    else if (i > n- 8.0) { gl_FragColor.rgb = ice(t);          }
    else if (i > n- 9.0) { gl_FragColor.rgb = fire(t);         }
    else if (i > n-10.0) { gl_FragColor.rgb = ice_and_fire(t); }
    else if (i > n-11.0) { gl_FragColor.rgb = reds(t);         }
    else if (i > n-12.0) { gl_FragColor.rgb = greens(t);       }
    else if (i > n-13.0) { gl_FragColor.rgb = blues(t);        }
    else if (i > n-14.0) { gl_FragColor.rgb = wheel(t);        }
    else if (i > n-15.0) { gl_FragColor.rgb = stripes(t);      }
    else if (i > n-16.0) { gl_FragColor.rgb = discrete(t);     }
    else if (i > n-17.0) { gl_FragColor.rgb = gray(-.05+1.1*t, vec3(1,0,0), vec3(0,0,1)); }


    gl_FragColor.a = 1.0;
    // Translate to gamma 2.2 space
    gl_FragColor.rgb = pow(gl_FragColor.rgb, vec3(1.0/2.2));
}
"""


window = app.Window(width=1600, height=800)

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
app.run(framerate=60)
