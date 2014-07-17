// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------

// Constants
// ------------------------------------
const float SQRT_2 = 1.4142135623730951;

// Uniforms
// ------------------------------------

// Externs
// ------------------------------------
// extern vec3  position;
// extern float size;
// extern float orientation;
// extern vec4  fg_color;
// extern vec4  bg_color;
// extern float antialias;
// extern float linewidth;

// Varyings
// ------------------------------------
varying float v_antialias;
varying float v_linewidth;
varying float v_size;
varying vec4  v_fg_color;
varying vec4  v_bg_color;
varying vec2  v_orientation;

// Main
// ------------------------------------
void main (void)
{
    // External definition of this function
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
