// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------

// Attributes
// -------------------------------------
attribute vec2 position;


// Main
// -------------------------------------
void main()
{
    gl_Position = vec4(position, 0.0, 1.0);
}
