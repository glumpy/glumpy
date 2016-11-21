// -----------------------------------------------------------------------------
// Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
// Distributed under the (new) BSD License.
// -----------------------------------------------------------------------------
#include "colormaps/util.glsl"

vec3 colormap_jet(float t)
{
    vec3 a, b;
    float c;
    if (t < 0.34) {
        a = vec3(0, 0, 0.5);
        b = vec3(0, 0.8, 0.95);
        c = (t - 0.0) / (0.34 - 0.0);
    } else if (t < 0.64) {
        a = vec3(0, 0.8, 0.95);
        b = vec3(0.85, 1, 0.04);
        c = (t - 0.34) / (0.64 - 0.34);
    } else if (t < 0.89) {
        a = vec3(0.85, 1, 0.04);
        b = vec3(0.96, 0.7, 0);
        c = (t - 0.64) / (0.89 - 0.64);
    } else {
        a = vec3(0.96, 0.7, 0);
        b = vec3(0.5, 0, 0);
        c = (t - 0.89) / (1.0 - 0.89);
    }
    return mix(a, b, c);
}

vec3 colormap_jet(float t, vec3 under, vec3 over)
{
    return colormap_underover(t, colormap_jet(t), under, over);
}

vec4 colormap_jet(float t, vec4 under, vec4 over)
{
    return colormap_underover(t, vec4(colormap_jet(t),1.0), under, over);
}
