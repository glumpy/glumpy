// -----------------------------------------------------------------------------
// Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
// Distributed under the (new) BSD License.
// -----------------------------------------------------------------------------
#ifndef __GEO_POSITION_STRUCT__
#define __GEO_POSITION_STRUCT__
struct GeoPosition
{
    vec2 position; // Actual position
    bool frozen;   // Prevent further transformation if true
};
#endif


vec4 position(float x)
{
    return vec4(x, 0.0, 0.0, 1.0);
}

vec4 position(float x, float y)
{
    return vec4(x, y, 0.0, 1.0);
}

vec4 position(vec2 xy)
{
    return vec4(xy, 0.0, 1.0);
}

vec4 position(float x, float y, float z)
{
    return vec4(x, y, z, 1.0);
}

vec4 position(vec3 xyz)
{
    return vec4(xyz, 1.0);
}

vec4 position(vec4 xyzw)
{
    return xyzw;
}

vec4 position(vec2 xy, float z)
{
    return vec4(xy, z, 1.0);
}

vec4 position(float x, vec2 yz)
{
    return vec4(x, yz, 1.0);
}

vec4 position(GeoPosition P)
{
    return vec4(P.position.xy, 0.0, 1.0);
}
