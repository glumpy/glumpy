#version 120

uniform sampler2D Velocity;
uniform sampler2D Temperature;
uniform sampler2D Density;
uniform float AmbientTemperature;
uniform float TimeStep;
uniform float Sigma;
uniform float Kappa;

vec4 texelFetch(sampler2D sampler, ivec2 P, int lod)
{
    return texture2D(sampler, vec2(P)/vec2(256.0,256.0));
}

void main()
{
    ivec2 TC = ivec2(gl_FragCoord.xy);
    float T = texelFetch(Temperature, TC, 0).r;
    vec2 V = texelFetch(Velocity, TC, 0).xy;

    gl_FragColor.rg = V;

    if (T > AmbientTemperature) {
        float D = texelFetch(Density, TC, 0).x;
        gl_FragColor.rg += (TimeStep * (T - AmbientTemperature) * Sigma - D * Kappa ) * vec2(0, 1);
    }
}
