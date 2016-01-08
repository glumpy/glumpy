// -----------------------------------------------------------------------------
// Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
// Distributed under the (new) BSD License.
// -----------------------------------------------------------------------------
#include "geo-position-struct.glsl"

GeoPosition geoposition(float x)
{
    GeoPosition position;
    position.longitude = x;
    position.latitude = 0.0;
    position.frozen = true;
    return position;
}

GeoPosition geoposition(float x, float y)
{
    GeoPosition position;
    position.longitude = x;
    position.latitude = y;
    position.frozen = false;
    return position;
}

GeoPosition geoposition(vec2 P)
{
    GeoPosition position;
    position.longitude = P.x;
    position.latitude = P.y;
    position.frozen = false;
    return position;
}

GeoPosition geoposition(float x, float y, float z)
{
    GeoPosition position;
    position.longitude = x;
    position.latitude = y;
    position.frozen = false;
    return position;
}

GeoPosition geoposition(vec3 P)
{
    GeoPosition position;
    position.longitude = P.x;
    position.latitude = P.y;
    position.frozen = false;
    return position;
}

GeoPosition geoposition(vec4 P)
{
    GeoPosition position;
    position.longitude = P.x;
    position.latitude = P.y;
    position.frozen = false;
    return position;
}

