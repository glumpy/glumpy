uniform sampler2D tex_data;
uniform vec2 tex_shape;
uniform vec4 color;

varying vec2 v_texcoord;
varying float v_scale;


vec4 Nearest(sampler2D texture, vec2 shape, vec2 uv);
vec4 Bilinear(sampler2D texture, vec2 shape, vec2 uv);
vec4 Hanning(sampler2D texture, vec2 shape, vec2 uv);
vec4 Hamming(sampler2D texture, vec2 shape, vec2 uv);
vec4 Hermite(sampler2D texture, vec2 shape, vec2 uv);
vec4 Kaiser(sampler2D texture, vec2 shape, vec2 uv);
vec4 Quadric(sampler2D texture, vec2 shape, vec2 uv);
vec4 Bicubic(sampler2D texture, vec2 shape, vec2 uv);
vec4 CatRom(sampler2D texture, vec2 shape, vec2 uv);
vec4 Mitchell(sampler2D texture, vec2 shape, vec2 uv);
vec4 Spline16(sampler2D texture, vec2 shape, vec2 uv);
vec4 Spline36(sampler2D texture, vec2 shape, vec2 uv);
vec4 Gaussian(sampler2D texture, vec2 shape, vec2 uv);
vec4 Bessel(sampler2D texture, vec2 shape, vec2 uv);
vec4 Sinc(sampler2D texture, vec2 shape, vec2 uv);
vec4 Lanczos(sampler2D texture, vec2 shape, vec2 uv);
vec4 Blackman(sampler2D texture, vec2 shape, vec2 uv);


vec4 Texture2D(sampler2D texture, vec2 shape, vec2 uv)
{
    if(v_scale > 5.0)
        return CatRom(texture,shape,uv);
    else
        return texture2D(texture, uv);
}


// smoothstep(lower edge0, upper edge1, x)
float contour(in float d, in float w)
{
    return smoothstep(0.5 - w, 0.5 + w, d);
}

float samp(in vec2 uv, float w)
{
    return contour(texture2D(tex_data, uv).r, w);
    // return contour(Bicubic(tex_data, tex_shape, uv).r, w);
    // return contour(Texture2D(tex_data, tex_shape, uv).r, w);
}

// The reciprocal of the square root of two (1/sqrt(2))
const float M_SQRT1_2 = 0.707106781186547524400844362104849039;

void main(void)
{

    // retrieve distance from texture
    vec2 uv = v_texcoord; //gl_TexCoord[0].xy;
    //float dist = texture2D(tex_data, uv).a;
    float dist = Texture2D(tex_data, tex_shape, v_texcoord).r;

    // fwidth helps keep outlines a constant width irrespective of scaling
    // GLSL's fwidth = abs(dFdx(uv)) + abs(dFdy(uv))
    float width = fwidth(dist);

    // supersampled version
    float alpha = contour( dist, width );

    if (v_scale < 1.0)
    {
        // Supersample, 4 extra points
        float dscale = 0.5 * M_SQRT1_2; // half of 1/sqrt2; you can play with this
        vec2 duv = dscale * (dFdx(uv) + dFdy(uv));
        vec4 box = vec4(uv-duv, uv+duv);
        float asum = samp( box.xy, width ) + samp( box.zw, width )
                   + samp( box.xw, width ) + samp( box.zy, width );

        // weighted average, with 4 extra points having 0.5 weight each,
        // so 1 + 0.5*4 = 3 is the divisor
        alpha = (alpha + 0.5 * asum) / 3.0;
    }

    gl_FragColor = vec4(color.rgb*alpha, alpha);
}
