# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
# High frequency (below pixel resolution) function plot
#
#  -> http://blog.hvidtfeldts.net/index.php/2011/07/plotting-high-frequency-functions-using-a-gpu/
#  -> https://www.shadertoy.com/view/4sB3zz
# -----------------------------------------------------------------------------
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
uniform vec2 iResolution;
uniform float iGlobalTime;

// --- Your function here ---
float function( float x )
{
    float d = 3.0 - 2.0*(1.0+cos(iGlobalTime/5.0))/2.0;
    return sin(pow(x,d))*sin(x);
}
// --- Your function here ---


float sample(vec2 uv)
{
    const int samples = 128;
    const float fsamples = float(samples);
    vec2 maxdist = vec2(0.5,1.0)/40.0;
    vec2 halfmaxdist = vec2(0.5) * maxdist;

    float stepsize = maxdist.x / fsamples;
    float initial_offset_x = -0.5 * fsamples * stepsize;
    uv.x += initial_offset_x;
    float hit = 0.0;
    for( int i=0; i<samples; ++i )
    {
        float x = uv.x + stepsize * float(i);
        float y = uv.y;
        float fx = function(x);
        float dist = abs(y-fx);
        hit += step(dist, halfmaxdist.y);
    }
    const float arbitraryFactor = 4.5;
    const float arbitraryExp = 0.95;
    return arbitraryFactor * pow( hit / fsamples, arbitraryExp );
}

void main(void)
{
    vec2 uv = gl_FragCoord.xy / iResolution.xy;
    float ymin = -2.0;
    float ymax = +2.0;
    float xmin = 0.0;
    float xmax = xmin + (ymax-ymin)* iResolution.x / iResolution.y;

    vec2 xy = vec2(xmin,ymin) + uv*vec2(xmax-xmin, ymax-ymin);
    gl_FragColor = vec4(0,0,0, sample(xy));
}
"""

window = app.Window(width=3*512, height=512, color=(1,1,1,1))
pause = False

@window.event
def on_draw(dt):
    window.clear()
    program.draw(gl.GL_TRIANGLE_STRIP)
    if not pause:
        program["iGlobalTime"] += dt

@window.event
def on_key_press(key, modifiers):
    global pause
    if key == ord(' '):
        pause = not pause

@window.event
def on_resize(width, height):
    program["iResolution"] = width, height

program = gloo.Program(vertex, fragment, count=4)
program['position'] = [(-1,-1), (-1,+1), (+1,-1), (+1,+1)]
program["iGlobalTime"] = 0
app.run()
