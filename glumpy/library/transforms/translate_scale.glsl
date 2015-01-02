// -----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier
// Distributed under the (new) BSD License. See LICENSE.txt for more info.
// -----------------------------------------------------------------------------
uniform vec3 scale;
uniform vec3 translate;

vec4 forward(vec4 position)
{
    return vec4(scale*position.xyz + translate, 1.0);
}

vec4 inverse(vec4 position)
{
    return vec4(position.xyz/scale - translate, 1.0);
}
