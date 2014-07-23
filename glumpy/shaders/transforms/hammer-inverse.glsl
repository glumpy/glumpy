// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------

/* ---------------------------------------------------------
   Inverse Hammer projection
   -> http://en.wikipedia.org/wiki/Hammer_projection

   Parameters:
   -----------

   position : 2d position in cartesian coordinates

   Return:
   -------
   2d position in (longitude,latitiude) coordinates

   --------------------------------------------------------- */

vec2 hammer_inverse(vec2 P)
{
    const float B = 2.0;
    float x = P.x;
    float y = P.y;
    float z = 1.0 - (x*x/16.0) - (y*y/4.0);
    // if (z < 0.0)
    //     discard;
    z = sqrt(z);
    float lon = 2.0*atan( (z*x),(2.0*(2.0*z*z - 1.0)));
    float lat = asin(z*y);
    return vec2(lon, lat);
}
