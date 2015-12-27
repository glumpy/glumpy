# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gl, gloo

vertex = """
#version 120

uniform vec2 mouse;
uniform float zoom;
attribute vec2 position;
varying float v_radius;
void main () {
    vec2 p = position - mouse;
    float d = length(p);
    p = normalize(p);
    v_radius = 2.0;

    if( d < 0.5 ) {
        float factor;
        float limit = 0.5;

        // Compute distortion factor
        if (d*zoom < limit) {
            factor = d*zoom;
            // Adapt radius to zoom level and point position
            v_radius = 2.0 + (0.50-d)*5.0 * min((zoom-1.0)/5.0,2.0);
        } else {
            factor = limit +(0.5-limit)*(d*zoom-limit)/(0.5*zoom-limit);
        }

        // Compute new position
        gl_Position = vec4(mouse + p*factor, 0.0, 1.0);

    } else {
        gl_Position = vec4(position, 0.0, 1.0);
    }
    gl_PointSize = 2.0*v_radius;
}
"""

fragment = """
#version 120

vec4 outline(float distance, float linewidth, float antialias, vec4 stroke, vec4 fill)
{
    vec4 frag_color;
    float t = linewidth/2.0 - antialias;
    float signed_distance = distance;
    float border_distance = abs(signed_distance) - t;
    float alpha = border_distance/antialias;
    alpha = exp(-alpha*alpha);
    if( border_distance < 0.0 )
        frag_color = stroke;
    else if( signed_distance < 0.0 )
        frag_color = mix(fill, stroke, sqrt(alpha));
    else
        frag_color = vec4(stroke.rgb, stroke.a * alpha);
    return frag_color;
}

varying float v_radius;
void main()
{
    vec4 stroke = vec4(0,0,0,1);
    vec4 fill = vec4(1,1,1,1);

    float distance = length(2.0*v_radius*gl_PointCoord.xy - vec2(v_radius));;
    gl_FragColor = outline(distance - (v_radius-1.0), 1, 1, stroke, fill);
}
"""

n = 25000
window = app.Window(1024,1024, color=(1,1,1,1))
program = gloo.Program(vertex, fragment, count=n)
program['position'] = np.random.normal(0.0,0.25,(n,2))
program['zoom'] = 2.0

@window.event
def on_mouse_motion(x, y, dx, dy):
    program['mouse'] = (2.0*float(x)/window.width-1.0,
                        1.0-2.0*float(y)/window.height)

@window.event
def on_mouse_scroll(x, y, dx, dy):
    zoom = program['zoom']
    program['zoom'] = min(max(zoom *(1.0+ dy/100.0), 1.0), 50.0)

@window.event
def on_draw(dt):
    window.clear()
    program.draw(gl.GL_POINTS)

app.run()
