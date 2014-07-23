// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------
#version 120

float marker(vec2 P, float size)
{
    const vec2 c1 = vec2(+0.25, 0.00);
    const vec2 c2 = vec2(-0.25, 0.00);
    float r1 = length(P-c1*size) - size/3;
    float r2 = length(P-c1*size) - size/7;
    float r3 = length(P-c2*size) - size/3;
    float r4 = length(P-c2*size) - size/7;
    return min( max(r1,-r2), max(r3,-r4));
}
