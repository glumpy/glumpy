// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------

// Constants
// ------------------------------------
const float SQRT_2 = 1.4142135623730951;

// Uniforms
// ------------------------------------
uniform mat4 u_model;
uniform mat4 u_view;
uniform mat4 u_projection;

// Externs
// ------------------------------------
// extern vec2  P0;
// extern vec2  P1;
// extern float index;
// extern vec4  fg_color;
// extern float antialias;
// extern float linewidth;

// Varyings
// ------------------------------------
varying float v_antialias;
varying float v_linewidth;
varying float v_size;
varying float v_texcoord;
varying vec4  v_fg_color;
varying vec4  v_bg_color;
varying vec2  v_orientation;

// Functions
// ------------------------------------
vec4 transform(vec3 position)
{
    return u_projection * u_view * u_model * vec4(position,1.0);
}

// Main
// ------------------------------------
void main (void)
{
    // This function is externally generated
    fetch_uniforms();

    v_size        = size;
    v_linewidth   = linewidth;
    v_antialias   = antialias;
    v_fg_color    = fg_color;
    v_bg_color    = bg_color;
    v_orientation = vec2(cos(orientation), sin(orientation));

    gl_Position = vec4(position, 1.0);
    gl_PointSize = SQRT_2 * size + 2.0 * (linewidth + 1.5*antialias);
}
