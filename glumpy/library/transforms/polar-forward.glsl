// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------
vec2 polar_forward(vec2 P)
{
    return vec2(P.x * cos(P.y), P.x * sin(P.y));
}

vec2 polar_forward(float x, float y)
{
    return polar_forward(vec2(x,y));
}

vec2 polar_forward(vec3 P)
{
    return polar_forward(P.xy);
}

vec2 polar_forward(vec4 P)
{
    return polar_forward(P.xy);
}
