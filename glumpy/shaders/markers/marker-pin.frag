// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------
#version 120

float f(vec2 p)
{
    return p.x*p.x*p.x*p.x*p.x + p.x*p.x*p.x*p.x - p.y*p.y;
}

vec2 grad(vec2 p )
{
    vec2 h = vec2( 0.001, 0.0 );
    return vec2( f(p+h.xy) - f(p-h.xy),
                 f(p+h.yx) - f(p-h.yx) )/(2.0*h.x);
}


float marker(vec2 P, float size)
{
/*
   const float SQRT_2 = 1.4142135623730951;
   float x = SQRT_2/2 * (P.x - P.y);
   float y = SQRT_2/2 * (P.x + P.y);
   float r1 = max(abs(x), abs(y)) - size/(2*SQRT_2);
   float r2 = length(P)-size/2.0;
   return max(min(P.y,r1),r2);
*/

/*
    vec2 c = vec2( 0.0, -0.25)*size;
    float r1 = length(P-c)-size/8.0;

    vec2 p = P.yx/(size) - vec2(0.5,0.0);
    float v = f(p);
    vec2  g = grad(p);
    float de = v/length(g);
    float r2 = max(-de*size, P.y-0.475*size);

    return max(-r1,r2);
*/

    vec2 c1 = vec2(0.0,-0.15)*size;
    float r1 = length(P-c1)-size/2.675;
    vec2 c2 = vec2(+1.49,-0.80)*size;
    float r2 = length(P-c2) - 2.*size;
    vec2 c3 = vec2(-1.49,-0.80)*size;
    float r3 = length(P-c3) - 2.*size;
    float r4 = length(P-c1)-size/5;
    return max( min(r1,max(max(r2,r3),-P.y)), -r4);

}
