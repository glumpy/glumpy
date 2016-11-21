// -----------------------------------------------------------------------------
// Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
// Distributed under the (new) BSD License.
// -----------------------------------------------------------------------------
#include "colormaps/util.glsl"


// Discrete
vec3 colormap_discrete(float t)
{
    return colormap_segment(0.0,0.2,t) * vec3(1,0,0)
         + colormap_segment(0.2,0.5,t) * vec3(0,1,0)
         + colormap_segment(0.5,1.0,t) * vec3(0,0,1);
}

vec3 colormap_discrete(float t, vec3 under, vec3 over)
{
    return colormap_underover(t, colormap_discrete(t), under, over);
}

vec4 colormap_discrete(float t, vec4 under, vec4 over)
{
    return colormap_underover(t, vec4(colormap_discrete(t),1.0), under, over);
}
