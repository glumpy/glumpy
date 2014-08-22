// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------
#version 120

float marker(vec2 P, float size)
{
    return max(abs(P.x)- size/2, abs(P.y)- size/6);
}
