#version 120

uniform sampler2D Sampler;
uniform vec3 FillColor;
uniform vec2 Scale;

void main()
{
    float L = texture2D(Sampler, gl_FragCoord.xy * Scale).r;
    gl_FragColor = vec4(FillColor, L);
}
