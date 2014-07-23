// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------


// Texture holding forward and inverse hammer projection
uniform sampler2D u_transform_texture;

vec2 forward(vec2 P) {
    P = (P - vec2(x2min,y2min)) / vec2(x2range,y2range);
    return texture2D(u_transform_texture,P).xy;
}
vec2 inverse(vec2 P) {
    P = (P - vec2(x1min,y1min)) / vec2(x1range,y1range);
    return texture2D(u_transform_texture, P).zw;
}
