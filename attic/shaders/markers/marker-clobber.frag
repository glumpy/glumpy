// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------
#version 120

float marker(vec2 P, float size)
{
    const float PI = 3.14159265358979323846264;

    const float t1 = -PI/2;
    const vec2  c1 = 0.25*vec2(cos(t1),sin(t1));

    const float t2 = t1+2*PI/3;
    const vec2  c2 = 0.25*vec2(cos(t2),sin(t2));

    const float t3 = t2+2*PI/3;
    const vec2  c3 = 0.25*vec2(cos(t3),sin(t3));

    float r1 = length( P - c1*size) - size/3.5;
    float r2 = length( P - c2*size) - size/3.5;
    float r3 = length( P - c3*size) - size/3.5;
    return min(min(r1,r2),r3);
}
