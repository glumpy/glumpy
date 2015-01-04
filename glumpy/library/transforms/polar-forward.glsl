// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------


/* ---------------------------------------------------------
   Forward polar projection

   Parameters:
   -----------

   position : 2d position in polar (rho,theta) coordinates

   Return:
   -------
   2d position in cartesian coordinates

   --------------------------------------------------------- */

vec2 transform_forward(vec2 P)
{
    float x = P.x * cos(P.y);
    float y = P.x * sin(P.y);
    return vec2(x,y);
}
