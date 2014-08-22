// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------
#version 120

float marker(vec2 P, float size)
{
    const float SQRT_2 = 1.4142135623730951;
    float x = P.x;
    float y = P.y;

    float r1 = max(abs(x)- size/2, abs(y)- size/6);
    float r2 = abs(x-size/1.5)+abs(y)-size;
    return max(r1,.75*r2);
}
