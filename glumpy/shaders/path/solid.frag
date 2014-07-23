// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------

// External functions (required)
// ------------------------------------
// vec4 stroke(float distance, float linewidth, float antialias, vec4 stroke);
// vec4 cap(int type, float dx, float dy, float linewidth, float antialias, vec4 stroke);

// Uniforms
// -------------------------------------
uniform float antialias;
uniform float linewidth;
uniform float miter_limit;
uniform float jointype;
uniform vec2  captypes;
uniform vec4  color;

// Varyings
// -------------------------------------
varying float v_length;
varying vec2  v_caps;
varying vec2  v_texcoord;
varying vec2  v_bevel_distance;


// Main
// -------------------------------------
void main()
{
    float distance = v_texcoord.y;
    vec4 color = vec4(0,0,0,1);

    if (v_caps.x < 0.0)
    {
        gl_FragColor = cap(1, v_texcoord.x, v_texcoord.y, linewidth, antialias, color);
        return;
    }
    else if (v_caps.y > v_length)
    {
        gl_FragColor = cap(1, v_texcoord.x-v_length, v_texcoord.y, linewidth, antialias, color);
        return;
    }

    // Round join (instead of miter)
    // if (v_texcoord.x < 0.0)          { distance = length(v_texcoord); }
    // else if(v_texcoord.x > v_length) { distance = length(v_texcoord - vec2(v_length, 0.0)); }

    float d = abs(distance) - linewidth/2.0 + antialias;

    // Miter limit
    float m = miter_limit*(linewidth/2.0);
    if (v_texcoord.x < 0.0)
    {
        d = max(v_bevel_distance.x-m ,d);
    }
    else if(v_texcoord.x > v_length)
    {
        d = max(v_bevel_distance.y-m ,d);
    }

    // gl_FragColor = stroke(d,  linewidth, antialias, color);

    float alpha = 1.0;
    if( d > 0.0 )
    {
        alpha = d/(antialias);
        alpha = exp(-alpha*alpha);
    }
    gl_FragColor = vec4(color.rgb, color.a*alpha);
}
