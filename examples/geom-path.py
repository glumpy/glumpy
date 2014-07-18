#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All rights reserved.
# Distributed under the terms of the new BSD License.
# -----------------------------------------------------------------------------
# This implements antialiased lines using a geometry shader with correct joins
# and caps.
# -----------------------------------------------------------------------------
import numpy as np
import glumpy as gp
import glumpy.gl as gl


vertex = """
#version 120
attribute vec2 position;
void main()
{
    gl_Position = vec4(position, 0.0, 1.0);
} """

fragment = """
#version 120
uniform float antialias;
uniform float linewidth;
uniform float miter_limit;

varying float v_length;
varying float v_alpha;
varying vec2 v_texcoord;
varying vec2 v_bevel_distance;

void main()
{
    float distance = v_texcoord.y;

    // Round join (instead of miter)
    // if (v_texcoord.x < 0.0)          { distance = length(v_texcoord); }
    // else if(v_texcoord.x > v_length) { distance = length(v_texcoord - vec2(v_length, 0.0)); }

    float d = abs(distance) - linewidth/2.0 + antialias;

    // Miter limit
    float m = miter_limit*(linewidth/2.0);
    if (v_texcoord.x < 0.0)          { d = max(v_bevel_distance.x-m ,d); }
    else if(v_texcoord.x > v_length) { d = max(v_bevel_distance.y-m ,d); }

    float alpha = 1.0;
    if( d > 0.0 )
    {
        alpha = d/(antialias);
        alpha = exp(-alpha*alpha);
    }
    gl_FragColor = vec4(0, 0, 0, alpha*v_alpha);
} """

geometry = """
#version 120
#extension GL_EXT_gpu_shader4 : enable
#extension GL_EXT_geometry_shader4 : enable

uniform mat4 projection;
uniform float antialias;
uniform float linewidth;
uniform float miter_limit;

varying out float v_length;
varying out float v_alpha;
varying out vec2 v_texcoord;
varying out vec2 v_bevel_distance;

float compute_u(vec2 p0, vec2 p1, vec2 p)
{
    // Projection p' of p such that p' = p0 + u*(p1-p0)
    // Then  u *= lenght(p1-p0)
    vec2 v = p1 - p0;
    float l = length(v);
    return ((p.x-p0.x)*v.x + (p.y-p0.y)*v.y) / l;
}

float line_distance(vec2 p0, vec2 p1, vec2 p)
{
    // Projection p' of p such that p' = p0 + u*(p1-p0)
    vec2 v = p1 - p0;
    float l2 = v.x*v.x + v.y*v.y;
    float u = ((p.x-p0.x)*v.x + (p.y-p0.y)*v.y) / l2;

    // h is the prpjection of p on (p0,p1)
    vec2 h = p0 + u*v;

    return length(p-h);
}

void main(void)
{
    // Get the four vertices passed to the shader
    vec2 p0 = gl_PositionIn[0].xy; // start of previous segment
    vec2 p1 = gl_PositionIn[1].xy; // end of previous segment, start of current segment
    vec2 p2 = gl_PositionIn[2].xy; // end of current segment, start of next segment
    vec2 p3 = gl_PositionIn[3].xy; // end of next segment

    // Determine the direction of each of the 3 segments (previous, current, next)
    vec2 v0 = normalize(p1 - p0);
    vec2 v1 = normalize(p2 - p1);
    vec2 v2 = normalize(p3 - p2);

    // Determine the normal of each of the 3 segments (previous, current, next)
    vec2 n0 = vec2(-v0.y, v0.x);
    vec2 n1 = vec2(-v1.y, v1.x);
    vec2 n2 = vec2(-v2.y, v2.x);

    // Determine miter lines by averaging the normals of the 2 segments
    vec2 miter_a = normalize(n0 + n1); // miter at start of current segment
    vec2 miter_b = normalize(n1 + n2); // miter at end of current segment

    // Determine the length of the miter by projecting it onto normal
    vec2 p,v;
    float d;
    float w = linewidth/2.0 + 1.5*antialias;
    v_length = length(p2-p1);

    float length_a = w / dot(miter_a, n1);
    float length_b = w / dot(miter_b, n1);

    float m = miter_limit*linewidth/2.0;

    // Angle between prev and current segment (sign only)
    float d0 = +1.0;
    if( (v0.x*v1.y - v0.y*v1.x) > 0 ) { d0 = -1.0;}

    // Angle between current and next segment (sign only)
    float d1 = +1.0;
    if( (v1.x*v2.y - v1.y*v2.x) > 0 ) { d1 = -1.0; }

    // Generate the triangle strip

    v_alpha = 1.0;
    // Cap at start
    if( p0 == p1 ) {
        p = p1 - w*v1 + w*n1;
        gl_Position = projection*vec4(p, 0.0, 1.0);
        v_texcoord = vec2(-w, +w);
        if (p2 == p3) v_alpha = 0.0;
    // Regular join
    } else {
        p = p1 + length_a * miter_a;
        gl_Position = projection*vec4(p, 0.0, 1.0);
        v_texcoord = vec2(compute_u(p1,p2,p), +w);
    }
    v_bevel_distance.x = +d0*line_distance(p1+d0*n0*w, p1+d0*n1*w, p);
    v_bevel_distance.y =    -line_distance(p2+d1*n1*w, p2+d1*n2*w, p);
    EmitVertex();

    v_alpha = 1.0;
    // Cap at start
    if( p0 == p1 ) {
        p = p1 - w*v1 - w*n1;
        v_texcoord = vec2(-w, -w);
        if (p2 == p3) v_alpha = 0.0;
    // Regular join
    } else {
        p = p1 - length_a * miter_a;
        v_texcoord = vec2(compute_u(p1,p2,p), -w);
    }
    gl_Position = projection*vec4(p, 0.0, 1.0);
    v_bevel_distance.x = -d0*line_distance(p1+d0*n0*w, p1+d0*n1*w, p);
    v_bevel_distance.y =    -line_distance(p2+d1*n1*w, p2+d1*n2*w, p);
    EmitVertex();

    v_alpha = 1.0;
    // Cap at end
    if( p2 == p3 ) {
        p = p2 + w*v1 + w*n1;
        v_texcoord = vec2(v_length+w, +w);
        if (p0 == p1) v_alpha = 0.0;
    // Regular join
    } else {
        p = p2 + length_b * miter_b;
        v_texcoord = vec2(compute_u(p1,p2,p), +w);
    }
    gl_Position = projection*vec4(p, 0.0, 1.0);
    v_bevel_distance.x =    -line_distance(p1+d0*n0*w, p1+d0*n1*w, p);
    v_bevel_distance.y = +d1*line_distance(p2+d1*n1*w, p2+d1*n2*w, p);
    EmitVertex();

    v_alpha = 1.0;
    // Cap at end
    if( p2 == p3 ) {
        p = p2 + w*v1 - w*n1;
        v_texcoord = vec2(v_length+w, -w);
        if (p0 == p1) v_alpha = 0.0;
    // Regular join
    } else {
        p = p2 - length_b * miter_b;
        v_texcoord = vec2(compute_u(p1,p2,p), -w);
    }
    gl_Position = projection*vec4(p, 0.0, 1.0);
    v_bevel_distance.x =    -line_distance(p1+d0*n0*w, p1+d0*n1*w, p);
    v_bevel_distance.y = -d1*line_distance(p2+d1*n1*w, p2+d1*n2*w, p);
    EmitVertex();

    EndPrimitive();
}
"""



# Nice spiral
n = 1024
T = np.linspace(0, 10*2*np.pi, n)
R = np.linspace(10, 400, n)
P = np.zeros((n,2), dtype=np.float32)
P[:,0] = 400 + np.cos(T)*R
P[:,1] = 400 + np.sin(T)*R

# Star
def star(inner=0.5, outer=1.0, n=5):
    R = np.array( [inner,outer]*n)
    T = np.linspace(0,2*np.pi,2*n,endpoint=False)
    P = np.zeros((2*n,2))
    P[:,0]= R*np.cos(T)
    P[:,1]= R*np.sin(T)
    return P

n = 12
miter_limit = 1.0
linewidth = 20.0
P = np.zeros((2*n+2,2),dtype=np.float32)
P[1:-1] = (star(n=12)*400 + (400,400)).astype(np.float32)
P[0] = P[1]
P[-1] = P[-2]



vertex   = gp.gloo.VertexShader(vertex)
fragment = gp.gloo.FragmentShader(fragment)
geometry = gp.gloo.GeometryShader(geometry,
                                  4, gl.GL_LINES_ADJACENCY_EXT, gl.GL_TRIANGLE_STRIP)
program = gp.gloo.Program(vertex, fragment, geometry)



window = gp.app.Window(width=800, height=800)

@window.event
def on_draw():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    program.draw(gl.GL_LINE_STRIP_ADJACENCY_EXT)

@window.event
def on_resize(width, height):
    gl.glViewport(0, 0, width, height)
    program['projection'] = gp.glm.ortho(0, width, 0, height, -1, +1)


gl.glClearColor(1.0, 1.0, 1.0, 1.0)
gl.glDisable(gl.GL_DEPTH_TEST)
gl.glEnable(gl.GL_BLEND)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)


program["position"] = P
program["linewidth"] = 10.0
program["antialias"] = 1.0
program["miter_limit"] = 4.0
gp.app.run()
