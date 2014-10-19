// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------

varying vec4  v_color;
varying float v_antialias;
varying float v_linewidth;
varying float v_miter_limit;
varying float v_length;
varying vec2  v_caps;
varying vec2  v_texcoord;
varying vec2  v_bevel_distance;


vec4 stroke(float distance, float linewidth, float antialias, vec4 stroke)
{
    vec4 frag_color;
    float t = linewidth/2.0 - antialias;
    float signed_distance = distance;
    float border_distance = abs(signed_distance) - t;
    float alpha = border_distance/antialias;
    alpha = exp(-alpha*alpha);

    if( border_distance > (linewidth/2.0 + antialias) )
        discard;
    else if( border_distance < 0.0 )
        frag_color = stroke;
    else
        frag_color = vec4(stroke.rgb, stroke.a * alpha);

    return frag_color;
}
vec4 cap(int type, float dx, float dy, float linewidth, float antialias, vec4 stroke)
{
    float d = 0.0;
    dx = abs(dx);
    dy = abs(dy);
    float t = linewidth/2.0 - antialias;

    // None
    if      (type == 0)  discard;
    // Round
    else if (type == 1)  d = sqrt(dx*dx+dy*dy);
    // Triangle in
    else if (type == 3)  d = (dx+abs(dy));
    // Triangle out
    else if (type == 2)  d = max(abs(dy),(t+dx-abs(dy)));
    // Square
    else if (type == 4)  d = max(dx,dy);
    // Butt
    else if (type == 5)  d = max(dx+t,dy);

    return stroke(d, linewidth, antialias, stroke);
}


void main()
{
//    gl_FragColor = vec4(0,0,0,1);

    float distance = v_texcoord.y;

    if (v_caps.x < 0.0)
    {
        gl_FragColor = cap(1, v_texcoord.x, v_texcoord.y,
                              v_linewidth, v_antialias, v_color);
        return;
    }
    if (v_caps.y > v_length)
    {
        gl_FragColor = cap(1, v_texcoord.x-v_length, v_texcoord.y,
                              v_linewidth, v_antialias, v_color);
        return;
    }

    // Round join (instead of miter)
    // if (v_texcoord.x < 0.0)          { distance = length(v_texcoord); }
    // else if(v_texcoord.x > v_length) { distance = length(v_texcoord - vec2(v_length, 0.0)); }

    // Miter limit
    float t = (v_miter_limit-1.0)*(v_linewidth/2.0) + v_antialias;

    if( (v_texcoord.x < 0.0) && (v_bevel_distance.x > (abs(distance) + t)) )
    {
        distance = v_bevel_distance.x - t;
    }
    else if( (v_texcoord.x > v_length) && (v_bevel_distance.y > (abs(distance) + t)) )
    {
        distance = v_bevel_distance.y - t;
    }
    gl_FragColor = stroke(distance, v_linewidth, v_antialias, v_color);
}
