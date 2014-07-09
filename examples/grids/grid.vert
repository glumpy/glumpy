// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------

// Model matrix (= identity)
uniform mat4  u_model;

// View matrix (= identity)
uniform mat4  u_view;

// Projection matrix (orthographic)
uniform mat4  u_projection;

// Vertex texture coordinate
attribute vec2 a_texcoord;

// Vertex position (in pixels)
attribute vec2 a_position;

// Texture coordinates are transferred to fragment shader
varying vec2 v_texcoord;

void main()
{
    gl_Position = u_projection * u_view * u_model * vec4(a_position, 0.0, 1.0);
    v_texcoord = a_texcoord;
}
