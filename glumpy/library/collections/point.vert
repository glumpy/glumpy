// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------
// Hooks:
//  <transform> : vec4 function(position, ...)
//
// ----------------------------------------------------------------------------
#version 120

// Collection externs
// ------------------------------------
// extern vec3  position;
// extern float size;
// extern vec4  color;

// Varyings
// ------------------------------------
varying float v_size;
varying vec4  v_color;

void main()
{
    // From collection
    fetch_uniforms();

    v_size = size;
    v_color = color;

    gl_Position = <transform>;
    gl_PointSize = size;
}
