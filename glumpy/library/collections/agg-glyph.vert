// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------

// Externs
// ------------------------------------
// vec2 origin;
// vec2 position;
// vec2 texcoord;
// vec4 color;

// Varyings
// ------------------------------------
varying vec4  v_color;
varying float v_offset;
varying vec2  v_texcoord;

// Main
// ------------------------------------
void main()
{
    fetch_uniforms();

    vec3 P = vec3(origin.xy + position, origin.z);
    // vec4(vec2(int(origin.x), origin.y) + position, origin.z,1.0);

    gl_Position = <transform(P)>;

    v_color = color;
    v_texcoord = texcoord;
    v_offset = 3.0*(offset + origin.x - int(origin.x));

    <viewport.transform>;
}
