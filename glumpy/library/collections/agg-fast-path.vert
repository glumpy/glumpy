// -----------------------------------------------------------------------------
// Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
// Distributed under the (new) BSD License.
// -----------------------------------------------------------------------------
// Hooks:
//  <transform> : vec4 function(position, ...)
//
// ----------------------------------------------------------------------------
#include "misc/viewport-NDC.glsl"

// Externs
// ------------------------------------
// extern vec3  prev;
// extern vec3  curr;
// extern vec3  next;
// extern float id;
// extern vec4  color;
// extern float antialias;
// extern float linewidth;

// Varyings
// ------------------------------------
varying float v_antialias;
varying float v_linewidth;
varying float v_distance;
varying vec4  v_color;


// Main
// ------------------------------------
void main (void)
{
    // This function is externally generated
    fetch_uniforms();
    v_linewidth = linewidth;
    v_antialias = antialias;
    v_color     = color;

    // transform prev/curr/next
    vec4 prev_ = <transform(prev)>;
    vec4 curr_ = <transform(curr)>;
    vec4 next_ = <transform(next)>;

    // prev/curr/next in viewport coordinates
    vec2 _prev = NDC_to_viewport(prev_, <viewport.viewport_global>.zw);
    vec2 _curr = NDC_to_viewport(curr_, <viewport.viewport_global>.zw);
    vec2 _next = NDC_to_viewport(next_, <viewport.viewport_global>.zw);

    // Compute vertex final position (in viewport coordinates)
    float w = linewidth/2.0 + 1.5*antialias;
    float z;
    vec2 P;
    if( curr == prev) {
        vec2 v = normalize(_next.xy - _curr.xy);
        vec2 normal = normalize(vec2(-v.y,v.x));
        P = _curr.xy + normal*w*id;
    } else if (curr == next) {
        vec2 v = normalize(_curr.xy - _prev.xy);
        vec2 normal  = normalize(vec2(-v.y,v.x));
        P = _curr.xy + normal*w*id;
    } else {
        vec2 v0 = normalize(_curr.xy - _prev.xy);
        vec2 v1 = normalize(_next.xy - _curr.xy);
        vec2 normal  = normalize(vec2(-v0.y,v0.x));
        vec2 tangent = normalize(v0+v1);
        vec2 miter   = vec2(-tangent.y, tangent.x);
        float l = abs(w / dot(miter,normal));
        P = _curr.xy + miter*l*sign(id);
    }

    if( abs(id) > 1.5 ) v_color.a = 0.0;

    v_distance = w*id;
    gl_Position = viewport_to_NDC(P, <viewport.viewport_global>.zw, curr_.z / curr_.w);

    <viewport.transform>;
}
