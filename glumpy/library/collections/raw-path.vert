// -----------------------------------------------------------------------------
// Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
// Distributed under the (new) BSD License.
// -----------------------------------------------------------------------------
// Hooks:
//  <transform> : vec4 function(position)
//
// ----------------------------------------------------------------------------

// Externs
// ------------------------------------
// extern vec3  position;
// extern float id;
// extern vec4  color;

// Varyings
// ------------------------------------
varying vec4 v_color;

// Main
// ------------------------------------
void main (void)
{
    fetch_uniforms();
    v_color = vec4(color.rgb, color.a*id);
    gl_Position = <transform(position)>;

    <viewport.transform>;
}
