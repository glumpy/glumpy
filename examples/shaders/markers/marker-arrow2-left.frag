// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------
#version 120

float marker(vec2 P, float size)
{
    const float SQRT_2 = 1.4142135623730951;
    float x = 1/SQRT_2 * (P.x - P.y);
    float y = 1/SQRT_2 * (P.x + P.y);

    float r1 = max(abs(x),        abs(y))        - size/3;
    float r2 = max(abs(x-size/5), abs(y-size/5)) - size/3;
    float r3 = max(abs(P.x-size/16)- size/3, abs(P.y)- size/10);
    return min(r3,max(r1,-r2));
}
