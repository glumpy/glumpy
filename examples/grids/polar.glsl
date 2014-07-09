// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------

// Constants
// ------------------------------------
const float M_PI = 3.14159265358979323846;

// Forward transform
// ------------------------------------
vec2 forward(vec2 P)
{
    float x = P.x * cos(P.y);
    float y = P.x * sin(P.y);
    return vec2(x,y);
}

// Inverse transform
// ------------------------------------
vec2 inverse(vec2 P)
{
    float rho = length(P);
    float theta = atan(P.y,P.x);
    if( theta < 0.0 )
        theta = 2.0*M_PI+theta;
    return vec2(rho,theta);
}
