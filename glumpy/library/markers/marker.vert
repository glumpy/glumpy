// -----------------------------------------------------------------------------
// Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
// Distributed under the (new) BSD License.
// -----------------------------------------------------------------------------
// Hooks:
//  <transform> : vec4 function(position, ...)
//
// ----------------------------------------------------------------------------
#include "math/constants.glsl"

// Uniforms
// ------------------------------------
uniform float antialias;

// Attributes
// ------------------------------------
attribute vec2  position;
attribute float size;
attribute vec4  fg_color;
attribute vec4  bg_color;
attribute float orientation;
attribute float linewidth;

// Varyings
// ------------------------------------
varying float v_size;
varying vec4  v_fg_color;
varying vec4  v_bg_color;
varying vec2  v_orientation;
varying float v_antialias;
varying float v_linewidth;

// Main (hooked)
// ------------------------------------
void main (void)
{
    v_size        = size;
    v_linewidth   = linewidth;
    v_antialias   = antialias;
    v_fg_color    = fg_color;
    v_bg_color    = bg_color;
    v_orientation = vec2(cos(orientation), sin(orientation));

    gl_Position = <transform>;
    gl_PointSize = M_SQRT2 * size + 2.0 * (linewidth + 1.5*antialias);
}
