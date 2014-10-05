#version 120

uniform sampler2D Sampler;
void main()
{
    gl_FragColor = texture2D(Sampler, gl_FragCoord.xy/256.0);
}
