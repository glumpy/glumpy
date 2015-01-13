// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------
#include "math/constants.glsl"

uniform float polar_origin;

vec2 forward(vec2 P)
{
    return vec2(P.x * cos(P.y+polar_origin),
                P.x * sin(P.y+polar_origin));
}

vec2 forward(float x, float y)
{
    return forward(vec2(x,y));
}

vec3 forward(vec3 P)
{
    return vec3(forward(P.xy), P.z);
}

vec4 forward(vec4 P)
{
    return vec4(forward(P.xy), P.z, P.w);
}

vec2 inverse(vec2 P)
{
    float rho = length(P);
    float theta = atan(P.y,P.x);
    if( theta < 0.0 )
        theta = 2.0*M_PI+theta;
    return vec2(rho,theta-polar_origin);
}

vec2 inverse(float x, float y)
{
    return inverse(vec2(x,y));
}

vec3 inverse(vec3 P)
{
    return vec3(inverse(P.xy), P.z);
}

vec4 inverse(vec4 P)
{
    return vec4(inverse(P.xy), P.z, P.w);
}
