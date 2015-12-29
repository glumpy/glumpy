// -----------------------------------------------------------------------------
// Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
// Distributed under the (new) BSD License.
// -----------------------------------------------------------------------------
uniform mat4 trackball_view;
uniform mat4 trackball_model;
uniform mat4 trackball_projection;

vec4 transform(vec4 position)
{
    return trackball_projection
           * trackball_view
           * trackball_model
           * position;
}
