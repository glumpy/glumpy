



uniform mat4 trackball_view;
uniform mat4 trackball_model;
uniform mat4 trackball_projection;
uniform vec2 trackball_pan;

vec4 transform(vec4 position)
{
    vec4 p =  trackball_projection * trackball_view * trackball_model * position;
    p.xy = trackball_pan * p.w + p.xy;
    return p;
}