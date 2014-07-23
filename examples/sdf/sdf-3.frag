#version 120

uniform sampler2D tex_data;
uniform vec2 tex_shape;
uniform vec4 color;

varying vec2 v_texcoord;

// #$input v_color0, v_texcoord0
// #include "../../common/common.sh"
//#SAMPLERCUBE(u_texColor, 0);

uniform float u_inverse_gamma;

void main()
{
    vec2 v_texcoord0 = v_texcoord;
    vec4 v_color0 = vec4(0,0,0,1);

//    int index = int(v_texcoord0.w*4.0 + 0.5);
    vec2 dx2 = dFdx(v_texcoord0.xy);
    vec2 dy2 = dFdy(v_texcoord0.xy);
    vec2 decal = 0.166667 * dx2;
    vec2 sampleLeft = v_texcoord0.xy - decal;
    vec2 sampleRight = v_texcoord0.xy + decal;

    // float left_dist = textureCube(u_texColor, sampleLeft).bgra[index];
    // float right_dist = textureCube(u_texColor, sampleRight).bgra[index];

    float left_dist = texture2D(tex_data, sampleLeft).r; //bgra[index];
    float right_dist = texture2D(tex_data, sampleRight).r; //bgra[index];

    //vec3 centerUV = 0.5 * (sampleLeft + sampleRight);
    //float dist = textureCube(u_texColor, centerUV).bgra[index];
    float dist = 0.5 * (left_dist + right_dist);

    float dx = length(dx2);
    float dy = length(dy2);
    float w = 16.0*0.5*(dx+dy);

    vec3 sub_color = smoothstep(0.5 -w, 0.5 + w, vec3(left_dist, dist, right_dist));
    gl_FragColor.rgb = 1.-sub_color*v_color0.a;
    //gl_FragColor.rgb = pow(gl_FragColor.rgb, vec3(u_inverse_gamma,u_inverse_gamma,u_inverse_gamma));
    gl_FragColor.a = dist*v_color0.a;

    //AR,AG,AB are the intensities gotten from the subpixel rendering engine.
    //BR,BG,BB are the old background pixels.
    //DR,DG,DB are the new background pixels.
    //DR = A*AR*R + (1-(A*AR))*BR
    //DG = A*AG*G + (1-(A*AG))*BG
    //DB = A*AB*B + (1-(A*AB))*BB
}
