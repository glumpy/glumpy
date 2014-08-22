// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------
#version 120

float marker(vec2 P, float size)
{
    const float SQRT_2 = 1.4142135623730951;
    float x = SQRT_2/1.5 * (-P.x + P.y) + size/12;
    float y = SQRT_2/1.5 * (-P.x - P.y) + size/12;

    float r1 = max(abs(x)- size/2, abs(y)- size/6);
    float r2 = max(abs(y-size/6)-size/3, abs(x-size/2)- size/6);
    return min(r1,r2);
}
