// -----------------------------------------------------------------------------
// Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
// Distributed under the (new) BSD License.
// -----------------------------------------------------------------------------
// From Fluid demo by Philip Rideout
// Originals sources and explanation on http://prideout.net/blog/?p=58
// -----------------------------------------------------------------------------
uniform sampler2D Velocity;
uniform sampler2D Pressure;
uniform sampler2D Obstacles;
uniform float GradientScale;
uniform vec2 InverseSize;

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

    vec3 oC = texelFetch(Obstacles, T, 0).xyz;
    if (oC.x > 0.0) {
        gl_FragColor.rg = oC.yz;
        return;
    }

    // Find neighboring pressure:
    float pN = texelFetchOffset(Pressure, T, 0, ivec2(0, 1)).r;
    float pS = texelFetchOffset(Pressure, T, 0, ivec2(0, -1)).r;
    float pE = texelFetchOffset(Pressure, T, 0, ivec2(1, 0)).r;
    float pW = texelFetchOffset(Pressure, T, 0, ivec2(-1, 0)).r;
    float pC = texelFetch(Pressure, T, 0).r;

    // Find neighboring obstacles:
    vec3 oN = texelFetchOffset(Obstacles, T, 0, ivec2(0, 1)).xyz;
    vec3 oS = texelFetchOffset(Obstacles, T, 0, ivec2(0, -1)).xyz;
    vec3 oE = texelFetchOffset(Obstacles, T, 0, ivec2(1, 0)).xyz;
    vec3 oW = texelFetchOffset(Obstacles, T, 0, ivec2(-1, 0)).xyz;

    // Use center pressure for solid cells:
    vec2 obstV = vec2(0.0);
    vec2 vMask = vec2(1.0);

    if (oN.x > 0.0) { pN = pC; obstV.y = oN.z; vMask.y = 0.0; }
    if (oS.x > 0.0) { pS = pC; obstV.y = oS.z; vMask.y = 0.0; }
    if (oE.x > 0.0) { pE = pC; obstV.x = oE.y; vMask.x = 0.0; }
    if (oW.x > 0.0) { pW = pC; obstV.x = oW.y; vMask.x = 0.0; }

    // Enforce the free-slip boundary condition:
    vec2 oldV = texelFetch(Velocity, T, 0).xy;
    vec2 grad = vec2(pE - pW, pN - pS) * GradientScale;
    vec2 newV = oldV - grad;
    gl_FragColor.rg = (vMask * newV) + obstV;
}
