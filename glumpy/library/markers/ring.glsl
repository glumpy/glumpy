// -----------------------------------------------------------------------------
// Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
// Distributed under the (new) BSD License.
// -----------------------------------------------------------------------------

float marker_ring(vec2 P, float size)
{
    float r1 = length(P) - size/2;
    float r2 = length(P) - size/4;
    return max(r1,-r2);
}
