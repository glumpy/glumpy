#version 120

uniform sampler2D VelocityTexture;
uniform sampler2D SourceTexture;
uniform sampler2D Obstacles;

uniform vec2 InverseSize;
uniform float TimeStep;
uniform float Dissipation;

void main()
{
    vec2 fragCoord = gl_FragCoord.xy;
    float solid = texture2D(Obstacles, InverseSize * fragCoord).x;
    if (solid > 0.0) {
        gl_FragColor = vec4(0);
        return;
    }

    vec2 u = texture2D(VelocityTexture, InverseSize * fragCoord).xy;
    vec2 coord = InverseSize * (fragCoord - TimeStep * u);
    gl_FragColor = Dissipation * texture2D(SourceTexture, coord);
}
