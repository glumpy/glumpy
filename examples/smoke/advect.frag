// -----------------------------------------------------------------------------
// Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
// Distributed under the (new) BSD License.
// -----------------------------------------------------------------------------
// From Fluid demo by Philip Rideout
// Originals sources and explanation on http://prideout.net/blog/?p=58
// -----------------------------------------------------------------------------
uniform sampler2D VelocityTexture;
uniform sampler2D SourceTexture;
uniform sampler2D Obstacles;

uniform vec2 InverseSize;
uniform float TimeStep;
uniform float Dissipation;

void main()
{
    vec2 fragCoord = InverseSize*gl_FragCoord.xy;
    float solid = texture2D(Obstacles, fragCoord).x;
    if (solid > 0.0) {
        gl_FragColor = vec4(0);
        return;
    }

    vec2 u = texture2D(VelocityTexture, fragCoord).xy;
    vec2 coord = fragCoord - InverseSize * TimeStep * u;
    gl_FragColor = Dissipation * texture2D(SourceTexture, coord);
}
