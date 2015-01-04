// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------

vec4 position2D(vec2 xy)
{
    return vec4(xy, 0.0, 1.0);
}

vec4 position2D(float x, float y)
{
    return vec4(x, y, 0.0, 1.0);
}
