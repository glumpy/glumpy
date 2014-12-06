// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------
// Hooks:
//  <transform> : vec4 function(position, ...)
//
// ----------------------------------------------------------------------------

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


vec2 NDC_to_viewport(vec4 position, vec2 viewport)
{
    vec2 p = position.xy/position.w;
    return (p+1.0)/2.0 * viewport;
}

vec4 viewport_to_NDC(vec2 position, vec2 viewport)
{
    return vec4(2.0*(position/viewport) - 1.0, 0.0, 1.0);
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

    vec4 P0_ = <transform(P0)>;
    vec4 P1_ = <transform(P1)>;

    // p0/p1 in viewport coordinates
    vec2 p0 = NDC_to_viewport(P0_, viewport.zw);
    vec2 p1 = NDC_to_viewport(P1_, viewport.zw);

    //
    vec2 position;
    vec2 T = p1 - p0;
    v_length = length(T);
    float w = v_linewidth/2.0 + 1.5*v_antialias;
    T = w*normalize(T);
    if( index < 0.5 ) {
       position = vec2( p0.x-T.y-T.x, p0.y+T.x-T.y);
       v_texcoord = vec2(-w, +w);
    } else if( index < 1.5 ) {
       position = vec2(p0.x+T.y-T.x, p0.y-T.x-T.y);
       v_texcoord= vec2(-w, -w);
    } else if( index < 2.5 ) {
       position = vec2( p1.x+T.y+T.x, p1.y-T.x+T.y);
       v_texcoord= vec2(v_length+w, -w);
    } else {
       position = vec2( p1.x-T.y+T.x, p1.y+T.x+T.y);
       v_texcoord = vec2(v_length+w, +w);
    }

    gl_Position = viewport_to_NDC(position, viewport.zw);


/*
    vec2 position;
    // vec2 T = P1 - P0;
    vec2 T = <transform(P1)>.xy - <transform(P0)>.xy;

    v_length = length(T);
    float w = v_linewidth/2.0 + 1.5*v_antialias;
    T = w*normalize(T);

    if( index < 0.5 ) {
       position = vec2( P0.x-T.y-T.x, P0.y+T.x-T.y);
       v_texcoord = vec2(-w, +w);
    } else if( index < 1.5 ) {
       position = vec2(P0.x+T.y-T.x, P0.y-T.x-T.y);
       v_texcoord= vec2(-w, -w);
    } else if( index < 2.5 ) {
       position = vec2( P1.x+T.y+T.x, P1.y-T.x+T.y);
       v_texcoord= vec2(v_length+w, -w);
    } else {
       position = vec2( P1.x-T.y+T.x, P1.y+T.x+T.y);
       v_texcoord = vec2(v_length+w, +w);
    }
    //gl_Position = <transform>;
    gl_Position = vec4(position,0,1);
*/
}
