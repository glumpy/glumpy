// -----------------------------------------------------------------------------
// Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
// Distributed under the (new) BSD License.
// -----------------------------------------------------------------------------
// From Fluid demo by Philip Rideout
// Originals sources and explanation on http://prideout.net/blog/?p=58
// -----------------------------------------------------------------------------
#include "misc/spatial-filters.frag"

uniform sampler2D u_data;
uniform vec2 u_shape;
uniform sampler2D Sampler;
uniform vec3 FillColor;
uniform vec2 Scale;
// vec2 Bicubic(sampler2D, vec2, vec2);

void main()
{
//    float L = texture2D(Sampler, gl_FragCoord.xy * Scale).r;
//    gl_FragColor = vec4(FillColor, L);
    vec2 texcoord = gl_FragCoord.xy * Scale;
    float v = Bicubic(u_data, u_shape, texcoord).r;
    gl_FragColor = vec4(FillColor, v);
}
