// -----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier
// Distributed under the (new) BSD License. See LICENSE.txt for more info.
// -----------------------------------------------------------------------------
vec4 forward(vec4 position)
{
    float x = position.x * cos(position.y);
    float y = position.x * sin(position.y);

    return vec4(x, y, position.z, 1.0);
}

vec4 inverse(vec4 position)
{
    float theta = atan(position.y, position.x);
    float rho = length(position.xy);

    return vec4(rho, theta, position.z, 1.0);
}
