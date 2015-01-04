// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------

vec4 position3D(vec3 xyz)
{
    return vec4(xyz, 1.0);
}

vec4 position3D(float x, float y, float z)
{
    return vec4(x, y, z, 1.0);
}

vec4 position3D(vec2 xy, float z)
{
    return vec4(xy, z, 1.0);
}

vec4 position3D(float x, vec2 yz)
{
    return vec4(x, yz, 1.0);
}
