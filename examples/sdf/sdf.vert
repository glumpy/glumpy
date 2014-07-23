uniform float scale;
attribute vec2 position;
attribute vec2 texcoord;
varying vec2 v_texcoord;
void main()
{
    gl_Position = vec4(scale*position, 0.0, 1.0);
    v_texcoord = texcoord;
}
