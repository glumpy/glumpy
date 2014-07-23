// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------

// Constants
// ------------------------------------

// Uniforms
// ------------------------------------
uniform float scale;


// Attributes
// ------------------------------------
attribute vec2 position;
attribute vec2 texcoord;

// Varyings
// ------------------------------------
varying vec2 v_texcoord;
varying float v_scale;


// Functions
// ------------------------------------
uniform mat4 model;
uniform mat4 projection;
uniform vec2 translate;
vec4 transform(vec4 position)
{
    projection*(vec4(translate,0,0)+model*vec4(scale*position, 0.0, 1.0));
}

// Main
// ------------------------------------
void main()
{
    gl_Position = transform(position, 0.0, 1.0);
    v_texcoord = texcoord;
    v_scale = scale;
}
