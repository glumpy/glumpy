// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------

// Constants
// ------------------------------------
const float M_PI    = 3.14159265358979323846;
const float M_SQRT2 = 1.41421356237309504880;


const float lambda0 = 0.0;
const float phi1    = 0.0;
float sin_phi1 = sin(phi1);
float cos_phi1 = cos(phi1);

// Forward transform
// ------------------------------------
vec2 forward(vec2 P)
{
    float lambda = P.x;
    float phi = P.y;

    float k = sqrt(2.0 / (1.0 + sin_phi1*sin(phi) + cos_phi1*cos(phi)*cos(lambda-lambda0)));
    float x = k * cos(phi) * sin(lambda-lambda0);
    float y = k * ( cos_phi1*sin(phi) -sin_phi1*cos(phi)*cos(lambda-lambda0));

    return vec2(x,y);
}

// Inverse transform
// ------------------------------------
vec2 inverse(vec2 P)
{
    float x = P.x;
    float y = P.y;

    float rho = sqrt(x*x+y*y);
//    if(rho > 2.0)
//        discard;
    float c = 2.0*asin(0.5*rho);

    float phi    = asin( cos(c) * sin_phi1 + y*sin(c)*cos_phi1/rho);
    float lambda = lambda0 + atan( x * sin(c), (rho*cos_phi1*cos(c) - y*sin_phi1*sin(c)));

    return vec2(lambda,phi);
}
