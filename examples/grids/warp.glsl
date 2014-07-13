// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------

// Constants
// ------------------------------------
const float M_PI = 3.14159265358979323846;

// Forward transform
// ------------------------------------
vec2 transform_forward(vec2 P)
{
    float rho = length(P);
    float r = (70.0-rho)/70.0;
    float theta = atan(P.y,P.x) + r * M_PI/3.0;
    float x = rho * cos(theta);
    float y = rho * sin(theta);
    return vec2(x,y);
}

// Inverse transform
// ------------------------------------
vec2 transform_inverse(vec2 P)
{
    float rho = length(P);
    float r = (70.0-rho)/70.0;
    float theta = atan(P.y,P.x) - r * M_PI/3.0;
    float x = rho * cos(theta);
    float y = rho * sin(theta);
    return vec2(x,y);
}
