// -----------------------------------------------------------------------------
// Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
// Distributed under the (new) BSD License.
// -----------------------------------------------------------------------------
#include "colormaps/util.glsl"


// By Morgan McGuire
vec3 colormap_stripes(float t)
{
    return vec3(mod(floor(t * 64.0), 2.0) * 0.2 + 0.8);
}

vec3 colormap_stripes(float t, vec3 under, vec3 over)
{
    return colormap_underover(t, colormap_stripes(t), under, over);
}

vec4 colormap_stripes(float t, vec4 under, vec4 over)
{
    return colormap_underover(t, vec4(colormap_stripes(t),1.0), under, over);
}
