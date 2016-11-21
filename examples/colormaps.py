# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
""" This example shows colormap functions (faster than 1d texture lookup) """

import datetime
from glumpy import app, gl, gloo

vertex = """
attribute vec2 position;
void main (void)
{
    gl_Position = vec4(position, 0.0, 1.0);
}
"""

fragment = """
#include "colormaps/colormaps.glsl"

uniform vec3      iResolution; // Viewport resolution (in pixels)
uniform float     iGlobalTime; // Shader playback time (in seconds)
uniform vec4      iMouse;      // Mouse pixel coords. xy: current (if MLB down) + zw: click
uniform vec4      iDate;       // Date as (year, month, day, time in seconds)
// uniform float     iChannelTime[4];       // Channel playback time (in seconds)
// uniform vec3      iChannelResolution[4]; // Channel resolution (in pixels)
// uniform sampler2D iChannel[4];           // Input channel. (XX = 2D or Cube)


void main(void)
{
    const float n = 18.0;

    vec2 uv = gl_FragCoord.xy / iResolution.xy;
    float t = gl_FragCoord.x / iResolution.x;

    // Discretization level
    // float levels = 32.0;
    // t = floor(t*levels)/levels;

    // Break up mach bands
    float i = n * gl_FragCoord.y / iResolution.y;

    if (mod(gl_FragCoord.y+n/4., iResolution.y / n) < max(iResolution.y / 200.0, 1.0))
    { gl_FragColor.rgb = vec3(0.0); }
    else if (i > n- 1.0) { gl_FragColor.rgb = colormap_gray(t);         }
    else if (i > n- 2.0) { gl_FragColor.rgb = colormap_hot(t);          }
    else if (i > n- 3.0) { gl_FragColor.rgb = colormap_cool(t);         }
    else if (i > n- 4.0) { gl_FragColor.rgb = colormap_autumn(t);       }
    else if (i > n- 5.0) { gl_FragColor.rgb = colormap_winter(t);       }
    else if (i > n- 6.0) { gl_FragColor.rgb = colormap_spring(t);       }
    else if (i > n- 7.0) { gl_FragColor.rgb = colormap_summer(t);       }
    else if (i > n- 8.0) { gl_FragColor.rgb = colormap_ice(t);          }
    else if (i > n- 9.0) { gl_FragColor.rgb = colormap_fire(t);         }
    else if (i > n-10.0) { gl_FragColor.rgb = colormap_icefire(t);      }
    else if (i > n-11.0) { gl_FragColor.rgb = colormap_reds(t);         }
    else if (i > n-12.0) { gl_FragColor.rgb = colormap_greens(t);       }
    else if (i > n-13.0) { gl_FragColor.rgb = colormap_blues(t);        }
    else if (i > n-14.0) { gl_FragColor.rgb = colormap_wheel(t);        }
    else if (i > n-15.0) { gl_FragColor.rgb = colormap_stripes(t);      }
    else if (i > n-16.0) { gl_FragColor.rgb = colormap_discrete(t);     }
    else if (i > n-17.0) { gl_FragColor.rgb = colormap_gray(-.05+1.1*t, vec3(1,0,0), vec3(0,0,1)); }
    else if (i > n-18.0) { gl_FragColor.rgb = colormap_jet(t);          }


    gl_FragColor.a = 1.0;
    // Translate to gamma 2.2 space
    gl_FragColor.rgb = pow(gl_FragColor.rgb, vec3(1.0/2.2));
}
"""


window = app.Window(width=1800, height=800)

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
