// -----------------------------------------------------------------------------
// Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
// Distributed under the (new) BSD License.
// -----------------------------------------------------------------------------
uniform vec4 viewport;    // in pixels
uniform vec2 iResolution; // in pixels
void clipping(void)
{
    vec2 position = gl_FragCoord.xy;
         if( position.x < (viewport.x)) discard;
    else if( position.x > (viewport.x+viewport.z)) discard;
    else if( position.y < (viewport.y)) discard;
    else if( position.y > (viewport.y+viewport.w)) discard;
}
