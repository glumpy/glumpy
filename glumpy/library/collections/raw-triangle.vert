// -----------------------------------------------------------------------------
// Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
// Distributed under the (new) BSD License.
// -----------------------------------------------------------------------------
// Hooks:
//  <transform> : vec4 function(position)
//
// ----------------------------------------------------------------------------
#version 120

// Externs
// ------------------------------------
// extern vec3 position;
// extern float size;
// extern vec4 color;

// Varyings
// ------------------------------------
varying vec4  v_color;

// Main (hooked)
// ------------------------------------
void main()
{
    fetch_uniforms();
    v_color = color;

    gl_Position = <transform(position)>;
}
