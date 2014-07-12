// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------

// Constants
// ------------------------------------
const float M_PI    = 3.14159265358979323846;
const float M_SQRT2 = 1.41421356237309504880;


// Forward transform
// ------------------------------------
vec2 forward(vec2 P)
{
    const float B = 2.0;
    float longitude = P.x;
    float latitude  = P.y;
    float cos_lat = cos(latitude);
    float sin_lat = sin(latitude);
    float cos_lon = cos(longitude/B);
    float sin_lon = sin(longitude/B);
    float d = sqrt(1.0 + cos_lat * cos_lon);
    float x = (B * M_SQRT2 * cos_lat * sin_lon) / d;
    float y =     (M_SQRT2 * sin_lat) / d;
    return vec2(x,y);
}

// Inverse transform
// ------------------------------------
vec2 inverse(vec2 P)
{
    const float B = 2.0;
    float x = P.x;
    float y = P.y;
    float z = 1.0 - (x*x/16.0) - (y*y/4.0);
    if (z < 0.0)
        discard;
    z = sqrt(z);
    float lon = 2.0*atan( (z*x),(2.0*(2.0*z*z - 1.0)));
    float lat = asin(z*y);
    return vec2(lon,lat);
}
