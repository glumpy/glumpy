// -----------------------------------------------------------------------------
// Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
// Distributed under the (new) BSD License.
// -----------------------------------------------------------------------------
#include "colormaps/util.glsl"

vec3 colormap_ice(float t)
{
   t = 1 - t;
   return mix(mix(vec3(1,1,1), vec3(0,1,1), t),
               mix(vec3(0,1,1), vec3(0,0,1), t*t), t);
}

vec3 colormap_ice(float t, vec3 under, vec3 over)
{
    return colormap_underover(t, colormap_ice(t), under, over);
}

vec4 colormap_ice(float t, vec4 under, vec4 over)
{
    return colormap_underover(t, vec4(colormap_ice(t),1.0), under, over);
}
