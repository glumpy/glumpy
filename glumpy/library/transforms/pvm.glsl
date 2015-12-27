// -----------------------------------------------------------------------------
// Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
// Distributed under the (new) BSD License.
// -----------------------------------------------------------------------------

uniform mat4 view;
uniform mat4 model;
uniform mat4 projection;

vec4 transform(vec4 position)
{
    return projection*view*model*position;
}
