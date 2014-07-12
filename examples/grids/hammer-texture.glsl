// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------

// Constants
// ------------------------------------
const float M_PI    = 3.14159265358979323846;
const float M_SQRT2 = 1.41421356237309504880;

// Texture holding forward and inverse hammer projection
uniform sampler2D u_hammer;

vec2 forward(vec2 P) {
    P = (P - vec2(x2min,y2min)) / vec2(x2range,y2range);
    return texture2D(u_hammer,P).xy;
}
vec2 inverse(vec2 P) {
    P = (P - vec2(x1min,y1min)) / vec2(x1range,y1range);
    return texture2D(u_hammer, P).zw;
}
