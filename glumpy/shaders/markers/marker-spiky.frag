// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------
#version 120

float marker(vec2 P, float size)
{
    const float PI = 3.14159265358979323846264;
    const float a = 0.55;
    const float b = 0.33;

    const float t1 = PI/2;
    const vec2  c1 = a*vec2(cos(t1),sin(t1));

    const float t2 = t1+2*PI/5;
    const vec2  c2 = a*vec2(cos(t2),sin(t2));

    const float t3 = t2+2*PI/5;
    const vec2  c3 = a*vec2(cos(t3),sin(t3));

    const float t4 = t3+2*PI/5;
    const vec2  c4 = a*vec2(cos(t4),sin(t4));

    const float t5 = t4+2*PI/5;
    const vec2  c5 = a*vec2(cos(t5),sin(t5));

    float r1 = length( P - c1*size) - b*size;
    float r2 = length( P - c2*size) - b*size;
    float r3 = length( P - c3*size) - b*size;
    float r4 = length( P - c4*size) - b*size;
    float r5 = length( P - c5*size) - b*size;
    return max(length(P) - size/2.5,
               -min(min(min(r1,r2),min(r3,r4)),r5));
}
