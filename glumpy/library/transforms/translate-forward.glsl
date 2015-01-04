// -----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier
// Distributed under the (new) BSD License. See LICENSE.txt for more info.
// -----------------------------------------------------------------------------
uniform vec3 translate_translate;

vec3 translate_forward(vec3 xyz)
{
    return vec4(xyz + translate_translate);
}

vec3 translate_forward(float x, float y, float z)
{
    return vec3(x,y,z) + translate_translate;
}

vec3 translate_forward(vec2 xy, float z)
{
    return vec3(xy,z) + translate_translate;
}

vec3 translate_forward(float x, vec2 yz)
{
    return vec3(x,yz) + translate_translate;
}
