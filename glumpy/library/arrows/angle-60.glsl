// -----------------------------------------------------------------------------
// Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
// Distributed under the (new) BSD License.
// -----------------------------------------------------------------------------
#include "arrows/util.glsl"

float arrow_angle_60(vec2 texcoord,
                     float body, float head,
                     float linewidth, float antialias)
{
    return arrow_angle(texcoord, body, head, 0.5, linewidth, antialias);
}
