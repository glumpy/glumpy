// -----------------------------------------------------------------------------
// Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
// Distributed under the (new) BSD License.
// -----------------------------------------------------------------------------
#include "colormaps/util.glsl"

vec3 colormap_ice(float t)
{
   return vec3(t, t, 1.0);
}

vec3 colormap_ice(float t, vec3 under, vec3 over)
{
    return colormap_underover(t, colormap_ice(t), under, over);
}

vec4 colormap_ice(float t, vec4 under, vec4 over)
{
    return colormap_underover(t, vec4(colormap_ice(t),1.0), under, over);
}
