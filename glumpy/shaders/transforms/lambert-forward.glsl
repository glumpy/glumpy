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

   position : 2d position in (longitude,latitiude) coordinates

   Return:
   -------
   2d position in cartesian coordinates

   --------------------------------------------------------- */

vec2 transform_forward(vec2 P)
{
    float lambda = P.x;
    float phi = P.y;
    float k = sqrt(2.0 / (1.0 + sin_phi1*sin(phi) + cos_phi1*cos(phi)*cos(lambda-lambda0)));
    float x = k * cos(phi) * sin(lambda-lambda0);
    float y = k * ( cos_phi1*sin(phi) -sin_phi1*cos(phi)*cos(lambda-lambda0));

    return vec2(x,y);
}
