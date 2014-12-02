// --- Projection/View/Model transformation ---
uniform mat4 view;
uniform mat4 model;
uniform mat4 projection;

vec4 transform(vec4 position)
{
    return projection*view*model*position;
}
