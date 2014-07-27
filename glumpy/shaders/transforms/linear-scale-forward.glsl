// --- Forward linear scaling ---
uniform vec3 scale;
vec4 forward(vec4 position)
{
    return vec4(position.xyz * scale, 1.0);
}
