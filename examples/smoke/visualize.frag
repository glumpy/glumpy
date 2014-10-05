// #version 120

vec2 Bicubic(sampler2D, vec2, vec2);

uniform sampler2D u_data;
uniform vec2 u_shape;

uniform sampler2D Sampler;
uniform vec3 FillColor;
uniform vec2 Scale;

void main()
{
//    float L = texture2D(Sampler, gl_FragCoord.xy * Scale).r;
//    gl_FragColor = vec4(FillColor, L);

    vec2 texcoord = gl_FragCoord.xy * Scale;
    gl_FragColor = vec4(FillColor, Bicubic(u_data, u_shape, texcoord).r);

}
