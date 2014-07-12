// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------

const float M_PI    = 3.14159265358979323846;
const float M_SQRT2 = 1.41421356237309504880;

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


// Texture holding forward (2 -> 1) and inverse  (1 -> 2) transform
uniform sampler2D u_transform;
uniform vec2 u_transform_shape;


// Compute transparency according to distance
float compute_alpha(float d, float width, float antialias)
{
    d -= width/2.0 - antialias;
    float alpha = d/antialias;
    return exp(-alpha*alpha);
}


// [0,1]x[0,1] -> [xmin,xmax]x[ymin,ymax]
vec2 scale_forward(vec2 P, vec4 limits)
{
    // limits = xmin,xmax,ymin,ymax
    P *= vec2(limits[1] - limits[0], limits[3]-limits[2]);
    P += vec2(limits[0], limits[2]);
    return P;
}

// [xmin,xmax]x[ymin,ymax] -> [0,1]x[0,1]
vec2 scale_inverse(vec2 P, vec4 limits)
{
    // limits = xmin,xmax,ymin,ymax
    P -= vec2(limits[0], limits[2]);
    P /= vec2(limits[1]-limits[0], limits[3]-limits[2]);
    return P;
}

//
vec2 transform_forward(vec2 P) {
    P = scale_inverse(P, u_limits2);

    vec2 epsilon = 1.0/u_transform_shape;
    P = epsilon/2.0 +(1.0-epsilon)*P;

    return texture2D(u_transform,P).xy;
}

//
vec2 transform_inverse(vec2 P) {
    P = scale_inverse(P, u_limits1);

    vec2 epsilon = 1.0/u_transform_shape;
    P = epsilon/2.0 +(1.0-epsilon)*P;

    return texture2D(u_transform, P).zw;
}


void main()
{
    vec2 P;
    vec2 NP1 = v_texcoord;
    vec2 P1 = scale_forward(NP1, u_limits1);
    vec2 P2 = transform_inverse(P1);

    if( P2.x < u_limits2[0]) discard;
    if( P2.x > u_limits2[1]) discard;
    if( P2.y < u_limits2[2]) discard;
    if( P2.y > u_limits2[3]) discard;

    vec2 NP2 = scale_inverse(P2,u_limits2);

    vec4 Tx = texture2D(u_grid, vec2(NP2.x, 0.5));
    vec4 Ty = texture2D(u_grid, vec2(NP2.y, 0.5));

    P = transform_forward(vec2(Tx.x,P2.y));
    P = scale_inverse(P, u_limits1);
    float Mx = length(a_size * (NP1 - P));

    P = transform_forward(vec2(Tx.y,P2.y));
    P = scale_inverse(P, u_limits1);
    float mx = length(a_size * (NP1 - P));

    P = transform_forward(vec2(P2.x,Ty.z));
    P = scale_inverse(P, u_limits1);
    float My = length(a_size * (NP1 - P));

    P = transform_forward(vec2(P2.x,Ty.w));
    P = scale_inverse(P, u_limits1);
    float my = length(a_size * (NP1 - P));

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
