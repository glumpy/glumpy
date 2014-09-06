#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gl, glm, gloo, shaders

vertex = """
    attribute vec2 position;
    void main()
    {
        gl_Position = vec4(position, 0.0, 1.0);
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

    // Within linestroke
    if( border_distance < 0.0 )
        frag_color = stroke;
    else if( signed_distance < 0.0 )
        // Inside shape
        if( border_distance > (linewidth/2.0 + antialias) )
            frag_color = fill;
        else // Line stroke interior border
            frag_color = mix(fill, stroke, alpha);
    else
        // Outide shape
        if( border_distance > (linewidth/2.0 + antialias) )
            discard;
        else // Line stroke exterior border
            frag_color = vec4(stroke.rgb, stroke.a * alpha);

    return frag_color;
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

vec4 filled(float distance, float linewidth, float antialias, vec4 fill)
{
    vec4 frag_color;
    float t = linewidth/2.0 - antialias;
    float signed_distance = distance;
    float border_distance = abs(signed_distance) - t;
    float alpha = border_distance/antialias;
    alpha = exp(-alpha*alpha);

    // Within linestroke
    if( border_distance < 0.0 )
        frag_color = fill;
    // Within shape
    else if( signed_distance < 0.0 )
        frag_color = fill;
    else
        // Outside shape
        if( border_distance > (linewidth/2.0 + antialias) )
            discard;
        else // Line stroke exterior border
            frag_color = vec4(fill.rgb, alpha * fill.a);

    return frag_color;
}

// Computes the signed distance from a line
float line_distance(vec2 p, vec2 p1, vec2 p2) {
    vec2 center = (p1 + p2) * 0.5;
    float len = length(p2 - p1);
    vec2 dir = (p2 - p1) / len;
    vec2 rel_p = p - center;
    return dot(rel_p, vec2(dir.y, -dir.x));
}

// Computes the signed distance from a line segment
float segment_distance(vec2 p, vec2 p1, vec2 p2) {
    vec2 center = (p1 + p2) * 0.5;
    float len = length(p2 - p1);
    vec2 dir = (p2 - p1) / len;
    vec2 rel_p = p - center;
    float dist1 = abs(dot(rel_p, vec2(dir.y, -dir.x)));
    float dist2 = abs(dot(rel_p, dir)) - 0.5*len;
    return max(dist1, dist2);
}

// Computes the center with given radius passing through p1 & p2
vec4 circle_from_2_points(vec2 p1, vec2 p2, float radius)
{
    float q = length(p2-p1);
    vec2 m = (p1+p2)/2.0;
    vec2 d = vec2( sqrt(radius*radius - (q*q/4.0)) * (p1.y-p2.y)/q,
                   sqrt(radius*radius - (q*q/4.0)) * (p2.x-p1.x)/q);
    return  vec4(m+d, m-d);
}

float arrow_curved(vec2 texcoord,
                   float body, float head,
                   float linewidth, float antialias)
{
    float w = linewidth/2.0 + antialias;
    vec2 start = -vec2(body/2.0, 0.0);
    vec2 end   = +vec2(body/2.0, 0.0);
    float height = 0.5;

    vec2 p1 = end - head*vec2(+1.0,+height);
    vec2 p2 = end - head*vec2(+1.0,-height);
    vec2 p3 = end;

    // Head : 3 circles
    vec2 c1  = circle_from_2_points(p1, p3, 1.25*body).zw;
    float d1 = length(texcoord - c1) - 1.25*body;
    vec2 c2  = circle_from_2_points(p2, p3, 1.25*body).xy;
    float d2 = length(texcoord - c2) - 1.25*body;
    vec2 c3  = circle_from_2_points(p1, p2, max(body-head, 1.0*body)).xy;
    float d3 = length(texcoord - c3) - max(body-head, 1.0*body);

    // Body : 1 segment
    float d4 = segment_distance(texcoord, start, end - vec2(linewidth,0.0));

    // Outside (because of circles)
    if( texcoord.y > +(2.0*head + antialias) )
         return 1000.0;
    if( texcoord.y < -(2.0*head + antialias) )
         return 1000.0;
    if( texcoord.x < -(body/2.0 + antialias) )
         return 1000.0;
    if( texcoord.x > c1.x ) //(body + antialias) )
         return 1000.0;

    return min( d4, -min(d3,min(d1,d2)));
}

float arrow_triangle(vec2 texcoord,
                     float body, float head, float height,
                     float linewidth, float antialias)
{
    float w = linewidth/2.0 + antialias;
    vec2 start = -vec2(body/2.0, 0.0);
    vec2 end   = +vec2(body/2.0, 0.0);

    // Head : 3 lines
    float d1 = line_distance(texcoord, end, end - head*vec2(+1.0,-height));
    float d2 = line_distance(texcoord, end - head*vec2(+1.0,+height), end);
    float d3 = texcoord.x - end.x + head;

    // Body : 1 segment
    float d4 = segment_distance(texcoord, start, end - vec2(linewidth,0.0));

    float d = min(max(max(d1, d2), -d3), d4);
    return d;
}

float arrow_triangle_90(vec2 texcoord,
                        float body, float head,
                        float linewidth, float antialias)
{
    return arrow_triangle(texcoord, body, head, 1.0, linewidth, antialias);
}

float arrow_triangle_60(vec2 texcoord,
                        float body, float head,
                        float linewidth, float antialias)
{
    return arrow_triangle(texcoord, body, head, 0.5, linewidth, antialias);
}

float arrow_triangle_30(vec2 texcoord,
                        float body, float head,
                        float linewidth, float antialias)
{
    return arrow_triangle(texcoord, body, head, 0.25, linewidth, antialias);
}

float arrow_angle(vec2 texcoord,
                  float body, float head, float height,
                  float linewidth, float antialias)
{
    float d;
    float w = linewidth/2.0 + antialias;
    vec2 start = -vec2(body/2.0, 0.0);
    vec2 end   = +vec2(body/2.0, 0.0);

    // Arrow tip (beyond segment end)
    if( texcoord.x > body/2.0) {
        // Head : 2 segments
        float d1 = line_distance(texcoord, end, end - head*vec2(+1.0,-height));
        float d2 = line_distance(texcoord, end - head*vec2(+1.0,+height), end);
        // Body : 1 segment
        float d3 = end.x - texcoord.x;
        d = max(max(d1,d2), d3);
    } else {
        // Head : 2 segments
        float d1 = segment_distance(texcoord, end - head*vec2(+1.0,-height), end);
        float d2 = segment_distance(texcoord, end - head*vec2(+1.0,+height), end);
        // Body : 1 segment
        float d3 = segment_distance(texcoord, start, end - vec2(linewidth,0.0));
        d = min(min(d1,d2), d3);
    }
    return d;
}

float arrow_angle_90(vec2 texcoord,
                     float body, float head,
                     float linewidth, float antialias)
{
    return arrow_angle(texcoord, body, head, 1.0, linewidth, antialias);
}

float arrow_angle_60(vec2 texcoord,
                        float body, float head,
                        float linewidth, float antialias)
{
    return arrow_angle(texcoord, body, head, 0.5, linewidth, antialias);
}

float arrow_angle_30(vec2 texcoord,
                        float body, float head,
                        float linewidth, float antialias)
{
    return arrow_angle(texcoord, body, head, 0.25, linewidth, antialias);
}


float arrow_stealth(vec2 texcoord,
                    float body, float head,
                    float linewidth, float antialias)
{
    float w = linewidth/2.0 + antialias;
    vec2 start = -vec2(body/2.0, 0.0);
    vec2 end   = +vec2(body/2.0, 0.0);
    float height = 0.5;

    // Head : 4 lines
    float d1 = line_distance(texcoord, end-head*vec2(+1.0,-height),
                                       end);
    float d2 = line_distance(texcoord, end-head*vec2(+1.0,-height),
                                       end-vec2(3.0*head/4.0,0.0));
    float d3 = line_distance(texcoord, end-head*vec2(+1.0,+height), end);
    float d4 = line_distance(texcoord, end-head*vec2(+1.0,+0.5),
                                       end-vec2(3.0*head/4.0,0.0));

    // Body : 1 segment
    float d5 = segment_distance(texcoord, start, end - vec2(linewidth,0.0));

    return min(d5, max( max(-d1, d3), - max(-d2,d4)));
}


// Constants
// ------------------------------------
const float SQRT_2 = 1.4142135623730951;

// External functions
// ------------------------------------
//float marker(vec2, float);
//vec4 filled(float, float, float, vec4);
//vec4 outline(float, float, float, vec4, vec4);
//vec4 stroke(float, float, float, vec4);


// Uniforms
// ------------------------------------
uniform float u_antialias;

// Varyings
// ------------------------------------
varying vec4  v_fg_color;
varying vec4  v_bg_color;
varying float v_linewidth;
varying float v_size;
varying vec2  v_rotation;

// Main
// ------------------------------------
void main()
{
    vec2 P = gl_PointCoord.xy - vec2(0.5,0.5);
    P = vec2(v_rotation.x*P.x - v_rotation.y*P.y,
             v_rotation.y*P.x + v_rotation.x*P.y) * v_size;

    float point_size = SQRT_2*v_size  + 2 * (v_linewidth + 1.5*u_antialias);
    float body = v_size/SQRT_2;

    // float d = arrow_curved(P, body, 0.25*body, v_linewidth, u_antialias);
    // float d = arrow_stealth(P, body, 0.25*body, v_linewidth, u_antialias);
    // float d = arrow_triangle_90(P, body, 0.15*body, v_linewidth, u_antialias);
    // float d = arrow_triangle_60(P, body, 0.20*body, v_linewidth, u_antialias);
    // float d = arrow_triangle_30(P, body, 0.25*body, v_linewidth, u_antialias);
    // float d = arrow_angle_90(P, body, 0.15*body, v_linewidth, u_antialias);
    float d = arrow_angle_60(P, body, 0.25*body, v_linewidth, u_antialias);
    // float d = arrow_angle_30(P, body, 0.33*body, v_linewidth, u_antialias);

    // gl_FragColor = outline(d, v_linewidth, u_antialias, v_fg_color, v_bg_color);
    gl_FragColor = filled(d, v_linewidth, u_antialias, v_fg_color);
    // gl_FragColor = stroke(d, v_linewidth, u_antialias, v_fg_color);
}
"""



# Create window
window = app.Window(width=2*512, height=512, color=(1,1,1,1))

# What to draw when necessary
@window.event
def on_draw(dt):
    window.clear()
    program.draw(gl.GL_POINTS)
    program['a_orientation'][-1] += np.pi/1024.0

# Setup ortho matrix on resize
@window.event
def on_resize(width, height):
    projection = glm.ortho(0, width, 0, height, -1, +1)
    program['u_projection'] = projection

# Setup some markers
n = 500+1
data = np.zeros(n, dtype=[('a_position',    np.float32, 3),
                          ('a_fg_color',    np.float32, 4),
                          ('a_bg_color',    np.float32, 4),
                          ('a_size',        np.float32, 1),
                          ('a_orientation', np.float32, 1),
                          ('a_linewidth',   np.float32, 1)])
data = data.view(gloo.VertexBuffer)
data['a_linewidth'] = 1
data['a_fg_color'] = 0, 0, 0, 1
data['a_bg_color'] = 1, 1, 1, 0
data['a_orientation'] = 0
radius, theta, dtheta = 245.0, 0.0, 6.5 / 180.0 * np.pi
for i in range(500):
    theta += dtheta
    x = 256 + radius * np.cos(theta)
    y = 256 + radius * np.sin(theta)
    r = 10.1 - i * 0.01
    radius -= 0.4
    data['a_orientation'][i] = theta + np.pi
    data['a_position'][i] = x, y, 0
    data['a_size'][i] = 2 * r
    data['a_linewidth'][i] = 1.5 - 0.5*i/500.

data['a_position'][n-1]    = 512+256, 256, 0
data['a_size'][n-1]        = 512/np.sqrt(2)
data['a_linewidth'][n-1]   = 16.0
data['a_fg_color'][n-1]    = 0, 0, 0, 1
data['a_bg_color'][n-1]    = .95, .95, .95, 1
data['a_orientation'][n-1] = 0

# Parse options to get marker
program = gloo.Program( shaders.get("marker.vert"), fragment)
program.bind(data)
program['u_antialias'] = 1.00
program['u_model'] = np.eye(4)
program['u_view'] = np.eye(4)
app.run()

"""
window = app.Window(width=800, height=800, color=(1,1,1,1))

@window.event
def on_draw(dt):
    window.clear()
    program.draw(gl.GL_TRIANGLE_STRIP)

@window.event
def on_resize(width, height):
    program["iResolution"] = width, height

program = gloo.Program(vertex, fragment, count=4)

dx,dy = 1,1
program['position'] = (-dx,-dy), (-dx,+dy), (+dx,-dy), (+dx,+dy)
app.run()
"""
