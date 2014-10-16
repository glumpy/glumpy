// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------

// Extern
// ------------------------------------
// extern vec2  position;
// extern vec4  color;
// extern float antialias;
// extern float linewidth;
// extern float miter_limit;

// Varyings
// ------------------------------------
varying vec4  v_geom_color[1];
varying float v_geom_antialias[1];
varying float v_geom_linewidth[1];
varying float v_geom_miter_limit[1];

void main()
{
    // Fetch uniforms
    fetch_uniforms();

    v_geom_color[0] = color;
    v_geom_antialias[0] = antialias;
    v_geom_linewidth[0] = linewidth;
    v_geom_miter_limit[0] = miter_limit;

    gl_Position = vec4(position.xy, 0.0, 1.0);
}
