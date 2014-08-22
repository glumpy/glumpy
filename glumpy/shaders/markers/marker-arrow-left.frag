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

    float r1 = abs(x) + abs(y) - size/2;
    float r2 = max(abs(x+size/2), abs(y)) - size/2;
    float r3 = max(abs(x-size/6)-size/4, abs(y)- size/4);
    return min(r3,max(.75*r1,r2));
}
