// -----------------------------------------------------------------------------
// Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
// Distributed under the (new) BSD License.
// -----------------------------------------------------------------------------
// From Fluid demo by Philip Rideout
// Originals sources and explanation on http://prideout.net/blog/?p=58
// -----------------------------------------------------------------------------
uniform vec2 InverseSize;
uniform sampler2D Sampler;
void main()
{
    gl_FragColor.rgb = texture2D(Sampler, gl_FragCoord.xy*InverseSize).rgb;
}
