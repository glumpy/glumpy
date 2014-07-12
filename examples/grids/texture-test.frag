varying vec2 v_texcoord;
uniform sampler1D u_texture;
uniform float u_texture_shape;

void main()
{
    float epsilon = 1.0/u_texture_shape;
    float x = epsilon/2.0 +(1.0-epsilon)*v_texcoord.x;
    float v = 32.0*abs(texture1D(u_texture,x).r -v_texcoord.x);
    gl_FragColor = vec4(v,v,v,1);
}
