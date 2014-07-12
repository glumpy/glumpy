// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------

// Compute transparency according to distance
float compute_alpha(float d, float width, float antialias)
{
    d -= width/2.0 - antialias;
    float alpha = d/antialias;
    return exp(-alpha*alpha);
}

// Forward transform
vec2 forward(vec2);

// Inverse transform
vec2 inverse(vec2);

// ----------------------------------------------------------------------------


// Line antialias area (usually 1 pixel)
uniform float u_antialias;

// Quad size
uniform vec2 a_size;

// Linear limits
uniform vec4 u_limits1;

// Spheric limits
uniform vec4 u_limits2;

// Major grid line width (1.50 pixel)
uniform float u_major_grid_width;

// Minor grid line width (0.75 pixel)
uniform float u_minor_grid_width;

// Major grid line color
uniform vec4 u_major_grid_color;

// Minor grid line color
uniform vec4 u_minor_grid_color;

// Texture holding normalized grid position
uniform sampler2D u_grid;

// Texture coordinates (from (-1,-1) to (+1,+1)
varying vec2 v_texcoord;


void main()
{
    float x1min   = u_limits1.x;
    float x1max   = u_limits1.y;
    float x1range = x1max - x1min;

    float y1min   = u_limits1.z;
    float y1max   = u_limits1.w;
    float y1range = y1max - y1min;

    float x2min   = u_limits2.x;
    float x2max   = u_limits2.y;
    float x2range = x2max - x2min;

    float y2min   = u_limits2.z;
    float y2max   = u_limits2.w;
    float y2range = y2max - y2min;

    float norm_x1 = v_texcoord.x;
    float norm_y1 = v_texcoord.y;

    float x1 = x1min + x1range * norm_x1;
    float y1 = y1min + y1range * norm_y1;

    vec2 P = inverse(vec2(x1,y1));
    float x2 = P.x;
    float y2 = P.y;

    if( x2 < x2min) discard;
    if( x2 > x2max) discard;
    if( y2 < y2min) discard;
    if( y2 > y2max) discard;

    float norm_x2 = (x2 - x2min) / x2range;
    float norm_y2 = (y2 - y2min) / y2range;

    vec4 T = texture2D(u_grid, vec2(norm_x2,0.5));

    P = forward(vec2(T.x,y2));
    P = (P - vec2(x1min,y1min)) / vec2(x1range,y1range);
    float Mx = length(a_size * (vec2(norm_x1,norm_y1) - P));

    P = forward(vec2(T.y,y2));
    P = (P - vec2(x1min,y1min)) / vec2(x1range,y1range);
    float mx = length(a_size * (vec2(norm_x1,norm_y1) - P));

    T = texture2D(u_grid, vec2(norm_y2,0.5));
    P = forward(vec2(x2,T.z));
    P = (P - vec2(x1min,y1min)) / vec2(x1range,y1range);
    float My = length(a_size * (vec2(norm_x1,norm_y1) - P));
    P = forward(vec2(x2,T.w));
    P = (P - vec2(x1min,y1min)) / vec2(x1range,y1range);
    float my = length(a_size * (vec2(norm_x1,norm_y1) - P));

    float M = min(Mx,My);
    float m = min(mx,my);

    vec4 color = u_major_grid_color;
    float alpha1 = compute_alpha( M, u_major_grid_width, u_antialias);
    float alpha2 = compute_alpha( m, u_minor_grid_width, u_antialias);
    float alpha  = alpha1;
    if( alpha2 > alpha1*1.5 )
    {
        alpha = alpha2;
        color = u_minor_grid_color;
    }
    gl_FragColor = vec4(color.rgb, color.a*alpha);
}
