// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------

// const float M_PI = 3.14159265358979323846;

/* ---------------------------------------------------------
   Forward polar projection

   Parameters:
   -----------

   position : 2d position in cartesian coordinates

   Return:
   -------

   2d position in polar (rho,theta) coordinates

   --------------------------------------------------------- */

vec2 transform_inverse(vec2 P)
{
    float rho = length(P);
    float theta = atan(P.y,P.x);
    //if( theta < 0.0 )
    //    theta = 2.0*M_PI+theta;
    return vec2(rho,theta);
}
