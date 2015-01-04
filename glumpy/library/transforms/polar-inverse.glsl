// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------
#include "math/constants.glsl"

vec2 polar_inverse(vec2 P)
{
    float rho = length(P);
    float theta = atan(P.y,P.x);
    if( theta < 0.0 )
        theta = 2.0*M_PI+theta;
    return vec2(rho,theta);
}

vec3 polar_inverse(vec3 P)
{
    return vec2( polar_inverse(P.xy), P.z);
}

vec4 polar_inverse(vec4 P)
{
    return vec2(polar_inverse(P.xy), P.z, P.w);
}
