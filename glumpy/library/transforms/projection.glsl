// -----------------------------------------------------------------------------
// Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
// Distributed under the (new) BSD License.
// -----------------------------------------------------------------------------
// Simple matrix projection
uniform mat4 projection;

vec4 transform(vec4 position)
{
    return projection*position;
}
