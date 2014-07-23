// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------

// Constants
// ------------------------------------

// Uniforms
// ------------------------------------
uniform float scale;

// Externs
// ------------------------------------
// vec4 color;
// vec2 position;
// vec2 texcoord;

// Varyings
// ------------------------------------
varying float v_scale;
varying vec2  v_texcoord;
varying vec4  v_color;


// Functions
// ------------------------------------
uniform mat4 model;
uniform mat4 projection;
vec4 transform(vec4 position)
{
    return projection*(vec4(translate,0,0) + model*vec4(scale*position.xy, 0.0, 1.0));
}

// Main
// ------------------------------------
void main()
{
    // This function is externally generated
    fetch_uniforms();

    gl_Position = transform( vec4(position,0,1) );
    v_texcoord = texcoord;
    v_scale = scale;
    v_color = color;
}
