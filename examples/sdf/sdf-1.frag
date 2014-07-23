uniform sampler2D tex_data;
uniform vec2      tex_shape;
uniform vec4      color;
varying vec2      v_texcoord;

vec4 Bicubic(sampler2D texture, vec2 shape, vec2 uv);

void main(void)
{
    // retrieve distance from texture
    // float dist = texture2D(texture, v_texcoord).r;
    float dist = Bicubic(tex_data, tex_shape, v_texcoord).r;

    // fwidth helps keep outlines a constant width irrespective of scaling
    float width = fwidth(dist);

    float alpha = smoothstep(0.5 - width, 0.5 + width, dist);

    // antialiased
    gl_FragColor = vec4(color.rgb, alpha);
}
