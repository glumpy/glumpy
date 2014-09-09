// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------
#version 120

// Constants
// ------------------------------------
const float SQRT_2 = 1.4142135623730951;

// External functions
// ------------------------------------
float marker(vec2, float);
vec4 filled(float, float, float, vec4);
vec4 outline(float, float, float, vec4, vec4);
vec4 stroke(float, float, float, vec4);


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
             v_rotation.y*P.x + v_rotation.x*P.y);

    float point_size = SQRT_2*v_size  + 2 * (v_linewidth + 1.5*u_antialias);

    float distance = marker(P*point_size, v_size);

    gl_FragColor = outline(distance, v_linewidth, u_antialias, v_fg_color, v_bg_color);
//    gl_FragColor = filled(distance, v_linewidth, u_antialias, v_fg_color);
//    gl_FragColor = stroke(distance, v_linewidth, u_antialias, v_fg_color);
}
