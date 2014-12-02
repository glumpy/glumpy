// --- Pan/Zoom ---
uniform vec2 scale;
uniform vec2 translate;
vec4 panzoom(vec4 position)
{
    return vec4(scale*position.xy + translate, position.z, 1.0);
}
