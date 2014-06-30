// -----------------------------------------------------------------------------
// Orthographic projection
// -----------------------------------------------------------------------------
uniform mat4 projection;

vec4 forward(vec4 position)
{
    return projection*position;
}
