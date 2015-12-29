# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
""" Voronoi shadertoy example from  www.shadertoy.com/view/ldl3W8 """

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


// I've not seen anybody out there computing correct cell interior distances for Voronoi
// patterns yet. That's why they cannot shade the cell interior correctly, and why you've
// never seen cell boundaries rendered correctly.

// However, here's how you do mathematically correct distances (note the equidistant and non
// degenerated grey isolines inside the cells) and hence edges (in yellow):

// http://www.iquilezles.org/www/articles/voronoilines/voronoilines.htm

#define ANIMATE

uniform vec2 iResolution;
uniform float iGlobalTime;
uniform float scale;

vec2 hash2( vec2 p )
{
    // procedural white noise
    return fract(sin(vec2(dot(p,vec2(127.1,311.7)),dot(p,vec2(269.5,183.3))))*43758.5453);
}

vec3 voronoi( in vec2 x )
{
    vec2 n = floor(x);
    vec2 f = fract(x);

    //----------------------------------
    // first pass: regular voronoi
    //----------------------------------
    vec2 mg, mr;

    float md = 8.0;
    for( int j=-1; j<=1; j++ )
    for( int i=-1; i<=1; i++ )
    {
        vec2 g = vec2(float(i),float(j));
        vec2 o = hash2( n + g);
    	#ifdef ANIMATE
            o = 0.5 + 0.5*sin( iGlobalTime + 6.2831*o );
        #endif
        vec2 r = g + o - f;
        float d = dot(r,r);

        if( d<md )
        {
            md = d;
            mr = r;
            mg = g;
        }
    }

    //----------------------------------
    // second pass: distance to borders
    //----------------------------------
    md = 8.0;
    for( int j=-2; j<=2; j++ )
    for( int i=-2; i<=2; i++ )
    {
        vec2 g = mg + vec2(float(i),float(j));
		vec2 o = hash2( n + g);
        #ifdef ANIMATE
            o = 0.5 + 0.5*sin( iGlobalTime + 6.2831*o );
        #endif
        vec2 r = g + o - f;
        if( dot(mr-r,mr-r)>0.00001 )
        md = min( md, dot( 0.5*(mr+r), normalize(r-mr) ) );
    }

    return vec3( md, mr );
}

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

void main( void )
{
    float s = scale/20.0;
    vec2 p = gl_FragCoord.xy/iResolution.xx - 0.5;
    vec3 c = voronoi( scale*p );

    // isolines
    vec3 color = c.x*(0.5 + 0.5*sin(64.0*c.x))*vec3(1.0);

    // borders
    color = mix( vec3(1.0,1.0,1.0), color, smoothstep( 0.03*s, 0.04*s, c.x ) );

    // feature points
    float dd = length( c.yz );
    color += vec3(1.0,1.0,0.0)*(1.0-smoothstep( 0.04*s, 0.05*s, dd));

    gl_FragColor = vec4(color,1.0);
}
"""


window = app.Window(width=800, height=800)

@window.event
def on_draw(dt):
    window.clear()
    program.draw(gl.GL_TRIANGLE_STRIP)
    program["iGlobalTime"] += dt

@window.event
def on_resize(width, height):
    program["iResolution"] = width, height

@window.event
def on_mouse_scroll(x, y, dx, dy):
    scale = program["scale"]
    program["scale"] = min(max(1, scale + .01 * dy * scale), 100)

program = gloo.Program(vertex, fragment, count=4)
program['position'] = [(-1,-1), (-1,+1), (+1,-1), (+1,+1)]
program["iGlobalTime"] = 0
program["scale"] = 10
app.run(framerate=60)
