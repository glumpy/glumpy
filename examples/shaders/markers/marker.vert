// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------
#version 120

// Constants
// ------------------------------------
const float SQRT_2 = 1.4142135623730951;

// Uniform
// ------------------------------------
uniform mat4  u_model;
uniform mat4  u_view;
uniform mat4  u_projection;
uniform float u_antialias;

// Attributes
// ------------------------------------
attribute float a_size;
attribute float a_orientation;
attribute vec3  a_position;
attribute float a_linewidth;
attribute vec4  a_fg_color;
attribute vec4  a_bg_color;

// Varyings
// ------------------------------------
varying float v_linewidth;
varying float v_size;
varying vec4  v_fg_color;
varying vec4  v_bg_color;
varying vec2  v_rotation;


// Main
// ------------------------------------
void main (void)
{
    v_size = a_size;
    v_linewidth = a_linewidth;
    v_fg_color = a_fg_color;
    v_bg_color = a_bg_color;
    v_rotation = vec2(cos(a_orientation), sin(a_orientation));
    gl_Position = u_projection  * u_view * u_model * vec4(a_position, 1.0);
    gl_PointSize = SQRT_2 * v_size + 2 * (a_linewidth + 1.5*u_antialias);
}
