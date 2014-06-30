// -----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier
// Distributed under the (new) BSD License. See LICENSE.txt for more info.
// -----------------------------------------------------------------------------
//
// Symetric logarithmic scaling transformation
//
// -----------------------------------------------------------------------------
uniform vec3 base;

vec4 forward(vec4 position)
{
    float x = position.x;
    float y = position.y;
    float z = position.z;

    if (base.x > 1.0)
        if (x > +1.0)
            x = +1 + log(+x) / log(base.x);
        else if (x < -1.0)
            x = -1 - log(-x) / log(base.x);

    if( (base.y > 1.0) && (y > 0.0) )
        if (y > +1.0)
            y = +1 + log(+y) / log(base.y);
        else if (y < -1.0)
            y = -1 - log(-y) / log(base.y);

    if( (base.z > 1.0) && (z > 0.0) )
        if (z > +1.0)
            z = +1 + log(+z) / log(base.z);
        else if (y < -1.0)
            z = -1 - log(-z) / log(base.z);

    return vec4(x, y, z, 1.0);
}

vec4 inverse(vec4 position)
{
    float x = position.x;
    float y = position.y;
    float z = position.z;

    if( (base.x > 1.0) )
        if (x > +1.0)
            x = +pow(base.x, +x-1);
        else if (x < -1.0)
            x = -pow(base.x, -x-1);

    if( (base.y > 1.0) )
        if (y > +1.0)
            y = +pow(base.y, +y-1);
        else if (y < -1.0)
            y = -pow(base.y, -y-1);

    if( (base.z > 1.0) )
        if (z > +1.0)
            z = +pow(base.z, +z-1);
        else if (z < -1.0)
            z = -pow(base.z, -z-1);

    return vec4(x, y, z, 1.0);
}
