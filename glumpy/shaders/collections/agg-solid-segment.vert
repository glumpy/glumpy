// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------

// Constants
// ------------------------------------

// Uniforms
// ------------------------------------
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

// Externs
// ------------------------------------
// extern vec2  P0;
// extern vec2  P1;
// extern float index;
// extern vec4  fg_color;
// extern float antialias;
// extern float linewidth;

// Varyings
// ------------------------------------
varying float v_length;
varying float v_antialias;
varying float v_linewidth;
varying vec2  v_texcoord;
varying vec4  v_fg_color;

// Functions
// ------------------------------------
vec4 transform(vec4 position)
{
    return projection * view * model * position;
}

// Main
// ------------------------------------
void main (void)
{
    // This function is externally generated
    fetch_uniforms();

    v_linewidth   = linewidth;
    v_antialias   = antialias;
    v_fg_color    = fg_color;

    vec2 P;
    vec2 T = P1 - P0;
    v_length = length(T);
    float w = linewidth/2.0 + 1.5*antialias;
    T = w*T/v_length;

    if( index < 0.5 ) {
       P = vec2( P0.x-T.y-T.x, P0.y+T.x-T.y);
       v_texcoord = vec2(-w, +w);
    } else if( index < 1.5 ) {
       P = vec2(P0.x+T.y-T.x, P0.y-T.x-T.y);
       v_texcoord= vec2(-w, -w);
    } else if( index < 2.5 ) {
       P = vec2( P1.x+T.y+T.x, P1.y-T.x+T.y);
       v_texcoord= vec2(v_length+w, -w);
    } else {
       P = vec2( P1.x-T.y+T.x, P1.y+T.x+T.y);
       v_texcoord = vec2(v_length+w, +w);
    }
    gl_Position = transform(vec4(P, 0.0, 1.0));
}
