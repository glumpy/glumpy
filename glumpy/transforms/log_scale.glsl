// -----------------------------------------------------------------------------
// Logarithmic scaling transformation
// -----------------------------------------------------------------------------
uniform vec3 base;

vec4 forward(vec4 position)
{
    float x = position.x;
    float y = position.y;
    float z = position.z;

    if( (base.x > 1.0) && (x > 0.0) )
        x = log(x) / log(base.x);
    if( (base.y > 1.0) && (y > 0.0) )
        y = log(y) / log(base.y);
    if( (base.z > 1.0) && (z > 0.0) )
        z = log(z) / log(base.z);

    return vec4(x, y, z, 1.0);
}

vec4 inverse(vec4 position)
{
    float x = position.x;
    float y = position.y;
    float z = position.z;

    if( (base.x > 1.0) )
        x = pow(base.x, x);
    if( (base.y > 1.0) )
        y = pow(base.y, y);
    if( (base.z > 1.0) )
        z = pow(base.z, z);

    return vec4(x, y, z, 1.0);
}
