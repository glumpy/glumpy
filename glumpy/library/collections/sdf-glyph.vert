// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------

// Externs
// ------------------------------------
// vec2 position;
// vec2 texcoord;
// vec3 origin;
// vec3 direction
// vec4 color;

// Varyings
// ------------------------------------
// varying float v_scale;
varying vec2  v_texcoord;
varying vec4  v_color;


// Functions
// ------------------------------------
uniform mat4 projection;
vec4 transform(vec2 position)
{
    return projection*(vec4(position.xy,0,1));
}

// Main
// ------------------------------------
void main()
{
    fetch_uniforms();

    vec3 tangent = normalize(direction);
    vec3 ortho   = cross(tangent, vec3(0,0,-1));
    gl_Position = transform( origin.xy+ vec2(400,400)
                             + tangent.xy*position.x
                             + ortho.xy*position.y );
    v_texcoord = texcoord;
    v_color = color;
}
