// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------
#version 120

float marker(vec2 P, float size)
{
    float r1 = max(abs(P.x - size/3), abs(P.x + size/3));
    float r2 = max(abs(P.y - size/3), abs(P.y + size/3));
    float r3 = max(abs(P.x), abs(P.y));
    float r = max(min(r1,r2),r3);
    r -= size/2;
    return r;
}
