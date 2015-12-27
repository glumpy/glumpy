// -----------------------------------------------------------------------------
// Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
// Distributed under the (new) BSD License.
// -----------------------------------------------------------------------------
// From Fluid demo by Philip Rideout
// Originals sources and explanation on http://prideout.net/blog/?p=58
// -----------------------------------------------------------------------------
uniform sampler2D Velocity;
uniform sampler2D Obstacles;
uniform vec2 InverseSize;
uniform float HalfInverseCellSize;

vec4 texelFetchOffset(sampler2D sampler, ivec2 P, int lod, ivec2 offset)
{
    return texture2D(sampler, vec2(P+offset)*InverseSize);
}

void main()
{
    ivec2 T = ivec2(gl_FragCoord.xy);

    // Find neighboring velocities:
    vec2 vN = texelFetchOffset(Velocity, T, 0, ivec2(0, 1)).xy;
    vec2 vS = texelFetchOffset(Velocity, T, 0, ivec2(0, -1)).xy;
    vec2 vE = texelFetchOffset(Velocity, T, 0, ivec2(1, 0)).xy;
    vec2 vW = texelFetchOffset(Velocity, T, 0, ivec2(-1, 0)).xy;

    // Find neighboring obstacles:
    vec3 oN = texelFetchOffset(Obstacles, T, 0, ivec2(0, 1)).xyz;
    vec3 oS = texelFetchOffset(Obstacles, T, 0, ivec2(0, -1)).xyz;
    vec3 oE = texelFetchOffset(Obstacles, T, 0, ivec2(1, 0)).xyz;
    vec3 oW = texelFetchOffset(Obstacles, T, 0, ivec2(-1, 0)).xyz;

    // Use obstacle velocities for solid cells:
    if (oN.x > 0.0) vN = oN.yz;
    if (oS.x > 0.0) vS = oS.yz;
    if (oE.x > 0.0) vE = oE.yz;
    if (oW.x > 0.0) vW = oW.yz;

    gl_FragColor.r = HalfInverseCellSize * (vE.x - vW.x + vN.y - vS.y);
}
