// -----------------------------------------------------------------------------
// Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
// Distributed under the (new) BSD License.
// -----------------------------------------------------------------------------
uniform mat4 arcball_view;
uniform mat4 arcball_model;
uniform mat4 arcball_projection;

vec4 transform(vec4 position)
{
    return arcball_projection
           * arcball_view
           * arcball_model
           * position;
}
