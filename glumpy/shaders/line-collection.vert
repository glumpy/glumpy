// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------

// Externs
// ------------------------------------
// vec3 position;
// vec4 color;
// void fetch_uniforms();

varying vec4 v_color;
void main()
{
    fetch_uniforms();
    v_color = color;
    gl_Position = vec4(position,1.0);
}
