// -----------------------------------------------------------------------------
// Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
// Distributed under the (new) BSD License.
// -----------------------------------------------------------------------------
// From Fluid demo by Philip Rideout
// Originals sources and explanation on http://prideout.net/blog/?p=58
// -----------------------------------------------------------------------------
uniform sampler2D Pressure;
uniform sampler2D Divergence;
uniform sampler2D Obstacles;
uniform vec2 InverseSize;
uniform float Alpha;
uniform float InverseBeta;

vec4 texelFetchOffset(sampler2D sampler, ivec2 P, int lod, ivec2 offset)
{
    return texture2D(sampler, vec2(P+offset)*InverseSize);
}
vec4 texelFetch(sampler2D sampler, ivec2 P, int lod)
{
    return texture2D(sampler, vec2(P)*InverseSize);
}


void main()
{
    ivec2 T = ivec2(gl_FragCoord.xy);

    // Find neighboring pressure:
    vec4 pN = texelFetchOffset(Pressure, T, 0, ivec2(0, 1));
    vec4 pS = texelFetchOffset(Pressure, T, 0, ivec2(0, -1));
    vec4 pE = texelFetchOffset(Pressure, T, 0, ivec2(1, 0));
    vec4 pW = texelFetchOffset(Pressure, T, 0, ivec2(-1, 0));
    vec4 pC = texelFetch(Pressure, T, 0);

    // Find neighboring obstacles:
    vec3 oN = texelFetchOffset(Obstacles, T, 0, ivec2(0, 1)).xyz;
    vec3 oS = texelFetchOffset(Obstacles, T, 0, ivec2(0, -1)).xyz;
    vec3 oE = texelFetchOffset(Obstacles, T, 0, ivec2(1, 0)).xyz;
    vec3 oW = texelFetchOffset(Obstacles, T, 0, ivec2(-1, 0)).xyz;

    // Use center pressure for solid cells:
    if (oN.x > 0.0) pN = pC;
    if (oS.x > 0.0) pS = pC;
    if (oE.x > 0.0) pE = pC;
    if (oW.x > 0.0) pW = pC;

    vec4 bC = texelFetch(Divergence, T, 0);
    gl_FragColor = (pW + pE + pS + pN + Alpha * bC) * InverseBeta;
}
