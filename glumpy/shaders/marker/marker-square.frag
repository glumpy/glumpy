// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------
#version 120

float marker(vec2 P, float size)
{
    const float SQRT_2 = 1.4142135623730951;

    return max(abs(P.x), abs(P.y)) - size/(2*SQRT_2);
}
