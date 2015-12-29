# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
""" Adaptation of https://www.shadertoy.com/view/4sS3zz """

import numpy as np
from glumpy import app, gl, glm, gloo

vertex = """
attribute vec2 position;
varying vec2 v_texcoord;
void main (void)
{
    gl_Position = vec4(position, 0.0, 1.0);
}
"""

fragment = """
// Created by inigo quilez - iq/2013
// License Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License.

// Analytical distance to an 2D ellipse, which is more complicated than it seems. It ends up being
// a quartic equation, which can be resolved through a cubic, then a quadratic. Some steps through the
// derivation can be found in this article:
//
// http://iquilezles.org/www/articles/ellipsedist/ellipsedist.htm
//

uniform vec2 iResolution;

vec4 stroke(float distance, float linewidth, float antialias, vec4 stroke)
{
    vec4 frag_color;
    float t = linewidth/2.0 - antialias;
    float signed_distance = distance;
    float border_distance = abs(signed_distance) - t;
    float alpha = border_distance/antialias;
    alpha = exp(-alpha*alpha);

    if( border_distance > (linewidth/2.0 + antialias) )
        discard;
    else if( border_distance < 0.0 )
        frag_color = stroke;
    else
        frag_color = vec4(stroke.rgb, stroke.a * alpha);

    return frag_color;
}

float sdEllipse(vec2 p, in vec2 ab )
{
    p = abs( p ); if( p.x > p.y ){ p=p.yx; ab=ab.yx; }
    float l = ab.y*ab.y - ab.x*ab.x;
    float m = ab.x*p.x/l;
    float n = ab.y*p.y/l;
    float m2 = m*m;
    float n2 = n*n;

    float c = (m2 + n2 - 1.0)/3.0;
    float c3 = c*c*c;

    float q = c3 + m2*n2*2.0;
    float d = c3 + m2*n2;
    float g = m + m*n2;

    float co;

    if(d < 0.0)
    {
        float p = acos(q/c3)/3.0;
        float s = cos(p);
        float t = sin(p)*sqrt(3.0);
        float rx = sqrt( -c*(s + t + 2.0) + m2 );
        float ry = sqrt( -c*(s - t + 2.0) + m2 );
        co = ( ry + sign(l)*rx + abs(g)/(rx*ry) - m)/2.0;
    }
    else
    {
        float h = 2.0*m*n*sqrt( d );
        float s = sign(q+h)*pow( abs(q+h), 1.0/3.0 );
        float u = sign(q-h)*pow( abs(q-h), 1.0/3.0 );
        float rx = -s - u - c*4.0 + 2.0*m2;
        float ry = (s - u)*sqrt(3.0);
        float rm = sqrt( rx*rx + ry*ry );
        float p = ry/sqrt(rm-rx);
        co = (p + 2.0*g/rm - m)/2.0;
    }

    float si = sqrt(1.0 - co*co);
    vec2 closestPoint = vec2(ab.x*co, ab.y*si);
    return length(closestPoint - p ) * sign(p.y-closestPoint.y);
}

void main(void)
{
    vec2 uv = gl_FragCoord.xy - iResolution.xy/2.;
    float d = sdEllipse(uv, vec2(.4,.1) * iResolution);

    // Outline
    gl_FragColor = stroke(abs(d), 50.0, 1.0, vec4(0,0,0,1));

    // Outline of outline
    // gl_FragColor = stroke(abs(d)-100.0, 5.0, 1.0, vec4(0,0,0,1));
}
"""


window = app.Window(width=800, height=800,
                    color=(1,1,1,1))

@window.event
def on_draw(dt):
    window.clear()
    program.draw(gl.GL_TRIANGLE_STRIP)

@window.event
def on_resize(width, height):
    program["iResolution"] = width, height

program = gloo.Program(vertex, fragment, count=4)
program['position'] = [(-1,-1), (-1,+1), (+1,-1), (+1,+1)]
gl.glEnable(gl.GL_BLEND)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
app.run(framerate=60)
