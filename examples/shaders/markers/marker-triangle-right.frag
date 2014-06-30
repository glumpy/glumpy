// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------
#version 120

float marker(vec2 P, float size)
{
   const float SQRT_2 = 1.4142135623730951;
   float x =  SQRT_2/2 * (P.x - P.y);
   float y = -SQRT_2/2 * (P.x + P.y);

   float r1 = max(abs(x), abs(y)) - size/(2*SQRT_2);
   float r2 = -P.x;

   return max(r1,r2);
}
