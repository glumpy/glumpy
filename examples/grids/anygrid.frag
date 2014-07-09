// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------
#version 120

// Constants
// ------------------------------------
const float M_PI    = 3.14159265358979323846;
const float M_SQRT2 = 1.41421356237309504880;

// Compute transparency according to distance
// ----------------------------------------------------------------------------
float compute_alpha(float d, float width, float antialias)
{
    d -= width/2.0 - antialias;
    float alpha = d/antialias;
    return exp(-alpha*alpha);
}

vec2 hammer_forward(vec2 P)
{
    const float B = 2.0;
    float latitude  = P.x;
    float longitude = P.y;
    float cos_lat = cos(latitude);
    float sin_lat = sin(latitude);
    float cos_lon = cos(longitude/B);
    float sin_lon = sin(longitude/B);
    float d = sqrt(1 + cos_lat * cos_lon);
    float x = (B * M_SQRT2 * cos_lat * sin_lon) / d;
    float y =     (M_SQRT2 * sin_lat) / d;
    return vec2(x,y);
}

vec2 hammer_inverse(vec2 P)
{
    const float B = 2.0;
    float x = P.x;
    float y = P.y;
    float z = 1 - (x*x/16.0) - (y*y/4.0);
    if (z < 0)
        discard;
    z = sqrt(z);
    float lon = 2*atan( (z*x),(2*(2*z*z - 1)));
    float lat = asin(z*y);
    return vec2(lon,lat);
}


vec2 forward(vec2 P) { return hammer_forward(P); }
vec2 inverse(vec2 P) { return hammer_inverse(P); }


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


// ----------------------------------------------------------------------------
void main()
{
    float xmin   = u_limits1.x;
    float xmax   = u_limits1.y;
    float xrange = xmax - xmin;

    float ymin   = u_limits1.z;
    float ymax   = u_limits1.w;
    float yrange = ymax - ymin;

    float lat_min   = u_limits2.x;
    float lat_max   = u_limits2.y;
    float lat_range = lat_max - lat_min;

    float lon_min   = u_limits2.z;
    float lon_max   = u_limits2.w;
    float lon_range = lon_max - lon_min;

    float x = xmin + xrange * v_texcoord.x;
    float y = ymin + yrange * v_texcoord.y;

    vec2 P = inverse(vec2(x,y));
    float longitude = P.x;
    float latitude = P.y;

    if( longitude <= lon_min) discard;
    if( longitude >= lon_max) discard;
    if( latitude  <= lat_min) discard;
    if( latitude  >= lat_max) discard;

    float normalized_longitude = (longitude - lon_min) / lon_range;
    float normalized_latitude  = (latitude  - lat_min) / lat_range;

    vec4 T = texture2D(u_grid, vec2(normalized_latitude,0.5));
    P = forward(vec2(T.x,longitude));
    P = (P - vec2(xmin,ymin)) / vec2(xrange,yrange);
    float Mx = length(a_size * (v_texcoord - P));

    P = forward(vec2(T.y,longitude));
    P = (P - vec2(xmin,ymin)) / vec2(xrange,yrange);
    float mx = length(a_size * (v_texcoord - P));

    T = texture2D(u_grid, vec2(normalized_longitude,0.5));
    P = forward(vec2(latitude,T.z));
    P = (P - vec2(xmin,ymin)) / vec2(xrange,yrange);
    float My = length(a_size * (v_texcoord - P));

    P = forward(vec2(latitude,T.w));
    P = (P - vec2(xmin,ymin)) / vec2(xrange,yrange);
    float my = length(a_size * (v_texcoord - P));

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
