// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------

const float lambda0 = 0.0;
const float phi1    = 0.0;
float sin_phi1 = sin(phi1);
float cos_phi1 = cos(phi1);

/* ---------------------------------------------------------
   Forward Lambert azimuthal equal-area projection
   -> http://en.wikipedia.org/wiki/Lambert_azimuthal_equal-area_projection

   Parameters:
   -----------

   position : 2d position in cartesian coordinates

   Return:
   -------
   2d position in (longitude,latitiude) coordinates

   --------------------------------------------------------- */

vec2 transform_inverse(vec2 P)
{
    float x = P.x;
    float y = P.y;

    float rho = sqrt(x*x+y*y);
    // if(rho > 2.0)
    //     discard;
    float c = 2.0*asin(0.5*rho);

    float phi    = asin( cos(c) * sin_phi1 + y*sin(c)*cos_phi1/rho);
    float lambda = lambda0 + atan( x * sin(c), (rho*cos_phi1*cos(c) - y*sin_phi1*sin(c)));

    return vec2(lambda, phi);
}
