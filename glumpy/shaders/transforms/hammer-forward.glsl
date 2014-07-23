// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------

const float M_SQRT2 = 1.41421356237309504880;

/* ---------------------------------------------------------
   Forward Hammer projection
   -> http://en.wikipedia.org/wiki/Hammer_projection

   Parameters:
   -----------

   position : 2d position in (longitude,latitiude) coordinates

   Return:
   -------
   2d position in cartesian coordinates

   --------------------------------------------------------- */

vec2 transform_forward(vec2 P)
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
