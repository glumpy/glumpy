// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------
#version 120

// Constants
// ------------------------------------
const float M_PI = 3.14159265358979323846;


// Compute transparency according to distance
// ----------------------------------------------------------------------------
float compute_alpha(float d, float width, float antialias)
{
    d -= width/2.0 - antialias;
    float alpha = d/antialias;
    return exp(-alpha*alpha);
}


// ----------------------------------------------------------------------------
// Line antialias area (usually 1 pixel)
uniform float u_antialias;

// Axis translation
uniform vec2 u_translate;

// Axis scale
uniform float u_scale;

// Axis x limit (theta)
uniform vec2 u_xlim;

// Axis y limit (rho)
uniform vec2 u_ylim;

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
    vec2 P = (v_texcoord - 2*(u_translate/1024.)) /u_scale;
    float radius = 1024/2.0 * u_scale;

    // Normalized y limits
    float ymin = u_ylim.x / u_ylim.y;
    float ymax = 1.0;

    // Normalized rho over[0,1]
    float rho = length(P);

    // Epsilon is used for ensuring at least linewidth outside main area
    float epsilon = (u_major_grid_width/2.0 + u_antialias)/radius;
    if( (rho < ymin-epsilon) || (rho > ymax+epsilon) )
    {
        discard;
    }

    bool outside = false;

    // Angle check
    float theta = atan(P.y,P.x);
    if( theta < 0 )
        theta = 2*M_PI+theta;

    // If we are very close to the upper limit (2pi), we take theta
    // complement such as to get the right distance from texture.
    epsilon = 1 * M_PI/180.0;
    if (theta > (2*M_PI - epsilon))
    {
        theta = 2*M_PI - theta;
//        if( (mod(u_xlim.x,360.0) - mod(u_xlim.y,360.0)) > 1.0 )
//        {
            outside = true;
//        }
    }

    epsilon = 1 * M_PI/180.0;
    if ( (theta < (u_xlim.x-epsilon)) || (theta > (u_xlim.y+epsilon)) )
    {
        discard;
    }

    // Renormalized rho over [ymin,ymax]
    float u = (rho - ymin) / (ymax-ymin);

    // Get nearest normalized major line
    float t;
    vec4 T = texture2D(u_grid, vec2(u,0.5));

    t = (T.x - u_ylim.x) / (u_ylim.y - u_ylim.x);
    float My = abs(u-t) * (1.0-ymin) * radius;

    // Get nearest normalized minor line
    t = (T.y - u_ylim.x) / (u_ylim.y - u_ylim.x);
    float my = abs(u-t) * (1.0-ymin) * radius;

    t = theta/(2*M_PI);
    T = 2*M_PI*texture2D(u_grid, vec2(t,0.5))/360.0;
    float Mx = abs(sin(theta-T.z) * (rho * radius));
    float mx = abs(sin(theta-T.w) * (rho * radius));

    float M = My;
    float m = my;

    if( (rho < ymin) && (rho > ymax) )
    {
        M = My;
        m = my;
    }

    // This test avoid circular lines to go outside limits
    // The external area is reserved for antaliasing start or ending lines
    else if ( ((theta < u_xlim.x) || (theta > u_xlim.y)) || outside )
    {
        M = Mx;
        m = mx;
    }

    // This test avoid straight lines to go outside limits
    // The external area is reserved for antaliasing inner or outer circle
    else if( (rho >= ymin) && (rho <= ymax) )
    {
        M = min(Mx,My);
        m = min(mx,my);
    }

    vec4 color = u_major_grid_color;
    float alpha1 = compute_alpha( M, u_major_grid_width, u_antialias);
    float alpha2 = compute_alpha( m, u_minor_grid_width, u_antialias);
    float alpha  = alpha1;
    if( alpha2 > alpha1*1.5 )
    {
        alpha = alpha2;
        color = u_minor_grid_color;
    }

    gl_FragColor = vec4(color.xyz, alpha*color.a);
}
