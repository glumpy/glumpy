// -----------------------------------------------------------------------------
// Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
// Distributed under the (new) BSD License.
// -----------------------------------------------------------------------------

float marker_vbar(vec2 P, float size)
{
    return max(abs(P.y)- size/2.0, abs(P.x)- size/6.0);
}
