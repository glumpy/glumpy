// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------
#version 120

// Constants
// ------------------------------------
const float SQRT_2 = 1.4142135623730951;

// External functions
// ------------------------------------
float marker(vec2 P, float size);

// Uniforms
// ------------------------------------
uniform float u_antialias;

// Varyings
// ------------------------------------
varying vec4  v_fg_color;
varying vec4  v_bg_color;
varying float v_linewidth;
varying float v_size;
varying vec2  v_rotation;

// Main
// ------------------------------------
void main()
{
    vec2 P = gl_PointCoord.xy - vec2(0.5,0.5);
    P = vec2(v_rotation.x*P.x - v_rotation.y*P.y,
             v_rotation.y*P.x + v_rotation.x*P.y);

    float point_size = SQRT_2*v_size  + 2 * (v_linewidth + 1.5*u_antialias);
    float t = v_linewidth/2.0 - u_antialias;
    float signed_distance = marker(P*point_size, v_size);
    float border_distance = abs(signed_distance) - t;
    float alpha = border_distance/u_antialias;
    alpha = exp(-alpha*alpha);

    // Within linestroke
    if( border_distance < 0 )
        gl_FragColor = v_fg_color;
    else if( signed_distance < 0 )
        // Inside shape
        if( border_distance > (v_linewidth/2.0 + u_antialias) )
            gl_FragColor = v_bg_color;
        else // Line stroke interior border
            gl_FragColor = mix(v_bg_color,v_fg_color,alpha);
    else
        // Outide shape
        if( border_distance > (v_linewidth/2.0 + u_antialias) )
            discard;
        else // Line stroke exterior border
            gl_FragColor = vec4(v_fg_color.rgb, v_fg_color.a * alpha);
}
