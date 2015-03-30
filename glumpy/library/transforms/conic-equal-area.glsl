// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------
#include "math/constants.glsl"

uniform float conic_scale;
uniform vec2  conic_center;
uniform vec2  conic_rotate;
uniform vec2  conic_translate;
uniform vec2  conic_parallels;
uniform vec4  conic_clip;

vec2 forward(float longitude, float latitude)
{
/*
    if( (conic_clip.x >= -180) && (longitude < conic_clip.x) )
        return vec2 (longitude, latitude);

    if( (conic_clip.y <= +180) && (longitude > conic_clip.y) )
        return vec2 (longitude, latitude);

    if( (conic_clip.z >= -90) && (latitude < conic_clip.z) )
        return vec2 (longitude, latitude);

    if( (conic_clip.w <= +90) && (latitude > conic_clip.w) )
        return vec2 (longitude, latitude);
*/

    float phi0 = conic_parallels.x * radian;
    float phi1 = conic_parallels.y * radian;

    longitude = (longitude + conic_rotate.x) * radian ;
    latitude  = (latitude  + conic_rotate.y) * radian;
    float n = (sin(phi0) + sin(phi1)) / 2.0;
    float C = 1.0 + sin(phi0) * (2.0*n - sin(phi0));
    float rho0 = sqrt(C) / n;
    float rho = sqrt(C - 2.0*n*sin(latitude))/n;
    vec2 P = vec2(       rho * sin(longitude * n),
                  rho0 - rho * cos(longitude*n)) + conic_center;
    return P*conic_scale + conic_translate;
}

vec2 forward(vec2 P) { return forward(P.x,P.y); }
vec3 forward(vec3 P) { return vec3(forward(P.x,P.y), P.z); }
vec4 forward(vec4 P) { return vec4(forward(P.x,P.y), P.z, P.w); }


/*
vec2 inverse(float x, float y)
{
    float phi0 = parallels.x;
    float phi1 = parallels.y;
    float n = (sin(phi0) + sin(phi1)) / 2.0;
    float C = 1.0 + sin(phi0) * (2.0*n - sin(phi0);
    float rho0 = sqrt(C) / n;

    float rho0_y = rho0 - y;
    return vec2( atan(x, rho0_y)/n,
                 asin((C - (x * x + rho0_y * rho0_y) * n * n) / (2.0 * n)));
}
vec2 inverse(vec2 P) { return inverse(P.x,P.y); }
vec3 inverse(vec3 P) { return vec3(inverse(P.x,P.y), P.z); }
vec4 inverse(vec4 P) { return vec4(inverse(P.x,P.y), P.z, P.w); }
*/
