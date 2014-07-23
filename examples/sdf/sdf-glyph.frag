// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------
// Ref: http://www.java-gaming.org/index.php?topic=33612.0
//      http://www.reddit.com/
//       -> r/gamedev/comments/2879jd/just_found_out_about_signed_distance_field_text/

// Constants
// ------------------------------------
// The reciprocal of the square root of two (1/sqrt(2))
const float M_SQRT1_2 = 0.707106781186547524400844362104849039;

// Uniforms
// ------------------------------------
uniform sampler2D atlas_data;
uniform vec2      atlas_shape;
uniform vec4      color;

// Varyings
// ------------------------------------
varying vec2 v_texcoord;
varying float v_scale;

// Functions
// ------------------------------------
vec4 Nearest(sampler2D texture, vec2 shape, vec2 uv);
vec4 Bilinear(sampler2D texture, vec2 shape, vec2 uv);
vec4 Bicubic(sampler2D texture, vec2 shape, vec2 uv);
vec4 CatRom(sampler2D texture, vec2 shape, vec2 uv);
vec4 Texture2D(sampler2D texture, vec2 shape, vec2 uv)
{
    if(v_scale > 5.0) return CatRom(texture,shape,uv);
    else              return texture2D(texture, uv);
}
float contour(in float d, in float w)
{
    return smoothstep(0.5 - w, 0.5 + w, d);
}
float sample(sampler2D texture, vec2 uv, float w)
{
    return contour(texture2D(texture, uv).r, w);
}


// Main
// ------------------------------------
void main(void)
{
    // Retrieve distance from texture
    float dist = Texture2D(atlas_data, atlas_shape, v_texcoord).r;

    // fwidth helps keep outlines a constant width irrespective of scaling
    // GLSL's fwidth = abs(dFdx(uv)) + abs(dFdy(uv))
    float width = fwidth(dist);

    // Regular SDF
    float alpha = contour( dist, width );

    // Supersampled version (when scale is small)
    if (v_scale < 1.0)
    {
        // Supersample, 4 extra points

        // Half of 1/sqrt2; you can play with this
        float dscale = 0.5 * M_SQRT1_2;
        vec2 duv = dscale * (dFdx(v_texcoord) + dFdy(v_texcoord));
        vec4 box = vec4(v_texcoord-duv, v_texcoord+duv);
        float asum = sample(atlas_data, box.xy, width)
                   + sample(atlas_data, box.zw, width)
                   + sample(atlas_data, box.xw, width)
                   + sample(atlas_data, box.zy, width);

        // weighted average, with 4 extra points having 0.5 weight each,
        // so 1 + 0.5*4 = 3 is the divisor
        alpha = (alpha + 0.5 * asum) / 3.0;
    }

    gl_FragColor = vec4(color.rgb*alpha, alpha);
}
