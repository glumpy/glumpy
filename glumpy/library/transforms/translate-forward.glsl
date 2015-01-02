// -----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier
// Distributed under the (new) BSD License. See LICENSE.txt for more info.
// -----------------------------------------------------------------------------
#ifndef __TRANSLATE__
#define __TRANSLATE__
uniform vec3 translate;
#endif

/* ---------------------------------------------------------
   Forward translate projection

   Parameters:
   -----------

   position : 3d position in cartesian coordinates

   Return:
   -------

   Translated position

   --------------------------------------------------------- */

vec4 translate_forward(vec4 position)
{
    return vec4(position.xyz + translate, position.w);
}
