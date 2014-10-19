// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------
// #version 120

// Externs
// ------------------------------------
// vec3 position;
// vec2 size;
// void fetch_uniforms();

void main()
{
    fetch_uniforms();

    gl_Position = <transform>;
    gl_PointSize = size;
}
