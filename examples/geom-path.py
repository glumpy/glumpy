# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
# This implements antialiased lines using a geometry shader with correct joins
# and caps.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gl, glm, gloo

# stride_tricks = np.lib.stride_tricks
# Z = np.arange(24,dtype=np.float32).reshape(8,3)
# stride_tricks.as_strided(Z,(4,4,12),(4,12,4)).reshape(16,4,3)

vertex = """
uniform float antialias;
uniform float linewidth;
uniform float miter_limit;

attribute vec2 position;

varying float v_antialias[1];
varying float v_linewidth[1];
varying float v_miter_limit[1];

void main()
{
    v_antialias[0] = antialias;
    v_linewidth[0] = linewidth;
    v_miter_limit[0] = miter_limit;

    gl_Position = vec4(position, 0.0, 1.0);
} """

fragment = """
vec4 stroke(float distance, float linewidth, float antialias, vec4 color)
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
        frag_color = color;
    else
        frag_color = vec4(color.rgb, color.a * alpha);

    return frag_color;
}
vec4 cap(int type, float dx, float dy, float linewidth, float antialias, vec4 color)
{
    float d = 0.0;
    dx = abs(dx);
    dy = abs(dy);
    float t = linewidth/2.0 - antialias;

    // None
    if      (type == 0)  discard;
    // Round
    else if (type == 1)  d = sqrt(dx*dx+dy*dy);
    // Triangle in
    else if (type == 3)  d = (dx+abs(dy));
    // Triangle out
    else if (type == 2)  d = max(abs(dy),(t+dx-abs(dy)));
    // Square
    else if (type == 4)  d = max(dx,dy);
    // Butt
    else if (type == 5)  d = max(dx+t,dy);

    return stroke(d, linewidth, antialias, color);
}


uniform vec4  color;
uniform float antialias;
uniform float linewidth;
uniform float miter_limit;

varying float v_length;
varying vec2  v_caps;
varying vec2  v_texcoord;
varying vec2  v_bevel_distance;

void main()
{
    float distance = v_texcoord.y;

    if (v_caps.x < 0.0)
    {
        gl_FragColor = cap(1, v_texcoord.x, v_texcoord.y, linewidth, antialias, color);
        return;
    }
    if (v_caps.y > v_length)
    {
        gl_FragColor = cap(1, v_texcoord.x-v_length, v_texcoord.y, linewidth, antialias, color);
        return;
    }

    // Round join (instead of miter)
    // if (v_texcoord.x < 0.0)          { distance = length(v_texcoord); }
    // else if(v_texcoord.x > v_length) { distance = length(v_texcoord - vec2(v_length, 0.0)); }

    // Miter limit
    float t = (miter_limit-1.0)*(linewidth/2.0) + antialias;

    if( (v_texcoord.x < 0.0) && (v_bevel_distance.x > (abs(distance) + t)) )
    {
        distance = v_bevel_distance.x - t;
    }
    else if( (v_texcoord.x > v_length) && (v_bevel_distance.y > (abs(distance) + t)) )
    {
        distance = v_bevel_distance.y - t;
    }
    gl_FragColor = stroke(distance, linewidth, antialias, color);
} """

geometry = """
#version 120
#extension GL_EXT_gpu_shader4 : enable
#extension GL_EXT_geometry_shader4 : enable

uniform mat4 projection;
// uniform float antialias;
// uniform float linewidth;
// uniform float miter_limit;

varying in float v_antialias[4][1];
varying in float v_linewidth[4][1];
varying in float v_miter_limit[4][1];

varying out vec2 v_caps;
varying out float v_length;
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

    // h is the projection of p on (p0,p1)
    vec2 h = p0 + u*v;

    return length(p-h);
}

void main(void)
{
    float antialias = v_antialias[0][0];
    float linewidth = v_linewidth[0][0];
    float miter_limit = v_miter_limit[0][0];


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

    // Cap at start
    if( p0 == p1 ) {
        p = p1 - w*v1 + w*n1;
        gl_Position = projection*vec4(p, 0.0, 1.0);
        v_texcoord = vec2(-w, +w);
        v_caps.x = v_texcoord.x;
    // Regular join
    } else {
        p = p1 + length_a * miter_a;
        gl_Position = projection*vec4(p, 0.0, 1.0);
        v_texcoord = vec2(compute_u(p1,p2,p), +w);
        v_caps.x = 1.0;
    }
    if( p2 == p3 ) v_caps.y = v_texcoord.x;
    else           v_caps.y = 1.0;

    v_bevel_distance.x = +d0*line_distance(p1+d0*n0*w, p1+d0*n1*w, p);
    v_bevel_distance.y =    -line_distance(p2+d1*n1*w, p2+d1*n2*w, p);
    EmitVertex();

    // Cap at start
    if( p0 == p1 ) {
        p = p1 - w*v1 - w*n1;
        v_texcoord = vec2(-w, -w);
        v_caps.x = v_texcoord.x;
    // Regular join
    } else {
        p = p1 - length_a * miter_a;
        v_texcoord = vec2(compute_u(p1,p2,p), -w);
        v_caps.x = 1.0;
    }
    if( p2 == p3 ) v_caps.y = v_texcoord.x;
    else           v_caps.y = 1.0;
    gl_Position = projection*vec4(p, 0.0, 1.0);
    v_bevel_distance.x = -d0*line_distance(p1+d0*n0*w, p1+d0*n1*w, p);
    v_bevel_distance.y =    -line_distance(p2+d1*n1*w, p2+d1*n2*w, p);
    EmitVertex();

    // Cap at end
    if( p2 == p3 ) {
        p = p2 + w*v1 + w*n1;
        v_texcoord = vec2(v_length+w, +w);
        v_caps.y = v_texcoord.x;
    // Regular join
    } else {
        p = p2 + length_b * miter_b;
        v_texcoord = vec2(compute_u(p1,p2,p), +w);
        v_caps.y = 1.0;
    }
    if( p0 == p1 ) v_caps.x = v_texcoord.x;
    else           v_caps.x = 1.0;

    gl_Position = projection*vec4(p, 0.0, 1.0);
    v_bevel_distance.x =    -line_distance(p1+d0*n0*w, p1+d0*n1*w, p);
    v_bevel_distance.y = +d1*line_distance(p2+d1*n1*w, p2+d1*n2*w, p);
    EmitVertex();

    // Cap at end
    if( p2 == p3 ) {
        p = p2 + w*v1 - w*n1;
        v_texcoord = vec2(v_length+w, -w);
        v_caps.y = v_texcoord.x;
    // Regular join
    } else {
        p = p2 - length_b * miter_b;
        v_texcoord = vec2(compute_u(p1,p2,p), -w);
        v_caps.y = 1.0;
    }
    if( p0 == p1 ) v_caps.x = v_texcoord.x;
    else           v_caps.x = 1.0;
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
def star(inner=0.45, outer=1.0, n=5):
    R = np.array( [inner,outer]*n)
    T = np.linspace(0,2*np.pi,2*n,endpoint=False)
    P = np.zeros((2*n,2))
    P[:,0]= R*np.cos(T)
    P[:,1]= R*np.sin(T)
    return P

vertex   = gloo.VertexShader(vertex)
fragment = gloo.FragmentShader(fragment)
geometry = gloo.GeometryShader(geometry, 4, gl.GL_LINES_ADJACENCY_EXT, gl.GL_TRIANGLE_STRIP)
program = gloo.Program(vertex, fragment, geometry)

P = (star(n=5)*350 + (400,400)).astype(np.float32)

closed = True
if closed:
    if np.allclose(P[0],P[1]):
        I = (np.arange(len(P)+2)-1)
        I[0], I[-1] = 0, len(P)-1
    else:
        I = (np.arange(len(P)+3)-1)
        I[0], I[-2], I[-1] = len(P)-1, 0, 1
else:
    I = (np.arange(len(P)+2)-1)
    I[0], I[-1] = 0, len(P)-1
I = I.astype(np.uint32).view(gloo.IndexBuffer)


program["position"] = P
program["linewidth"] = 13.0
program["antialias"] = 1.0
program["miter_limit"] = 4.0
program["color"] = 0,0,0,1

window = app.Window(width=800, height=800, color=(1,1,1,1))

@window.event
def on_draw(dt):
    window.clear()
    program.draw(gl.GL_LINE_STRIP_ADJACENCY_EXT, I)

@window.event
def on_resize(width, height):
    program['projection'] = glm.ortho(0, width, 0, height, -1, +1)

app.run()
