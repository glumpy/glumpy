// -----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// -----------------------------------------------------------------------------

// --- disc
float disc(vec2 P, float size)
{
    return length(P) - size/2;
}

// --- square
float square(vec2 P, float size)
{
    return max(abs(P.x), abs(P.y)) - size/(2*SQRT_2);
}

// --- triangle
float triangle(vec2 P, float size)
{
   float x = SQRT_2/2 * (P.x - P.y);
   float y = SQRT_2/2 * (P.x + P.y);
   float r1 = max(abs(x), abs(y)) - size/(2*SQRT_2);
   float r2 = P.y;
   return max(r1,r2);
}

// --- diamond
float diamond(vec2 P, float size)
{
   float x = SQRT_2/2 * (P.x - P.y);
   float y = SQRT_2/2 * (P.x + P.y);
   return max(abs(x), abs(y)) - size/(2*SQRT_2);
}

// --- heart
float marker(vec2 P, float size)
{
   float x = SQRT_2/2.0 * (P.x - P.y);
   float y = SQRT_2/2.0 * (P.x + P.y);
   float r1 = max(abs(x),abs(y))-size/3.5;
   float r2 = length(P - SQRT_2/2.0*vec2(+1.0,-1.0)*size/3.5) - size/3.5;
   float r3 = length(P - SQRT_2/2.0*vec2(-1.0,-1.0)*size/3.5) - size/3.5;
   return min(min(r1,r2),r3);
}

// --- spade
float spade(vec2 P, float size)
{
   // Reversed heart (diamond + 2 circles)
   float s= size * 0.85 / 3.5;
   float x = SQRT_2/2.0 * (P.x + P.y) + 0.4*s;
   float y = SQRT_2/2.0 * (P.x - P.y) - 0.4*s;
   float r1 = max(abs(x),abs(y)) - s;
   float r2 = length(P - SQRT_2/2.0*vec2(+1.0,+0.2)*s) - s;
   float r3 = length(P - SQRT_2/2.0*vec2(-1.0,+0.2)*s) - s;
   float r4 =  min(min(r1,r2),r3);

   // Root (2 circles and 2 planes)
   const vec2 c1 = vec2(+0.65, 0.125);
   const vec2 c2 = vec2(-0.65, 0.125);
   float r5 = length(P-c1*size) - size/1.6;
   float r6 = length(P-c2*size) - size/1.6;
   float r7 = P.y - 0.5*size;
   float r8 = 0.1*size - P.y;
   float r9 = max(-min(r5,r6), max(r7,r8));

    return min(r4,r9);
}

// --- club
float club(vec2 P, float size)
{
    // clover (3 discs)
    const float t1 = -PI/2.0;
    const vec2  c1 = 0.225*vec2(cos(t1),sin(t1));
    const float t2 = t1+2*PI/3.0;
    const vec2  c2 = 0.225*vec2(cos(t2),sin(t2));
    const float t3 = t2+2*PI/3.0;
    const vec2  c3 = 0.225*vec2(cos(t3),sin(t3));
    float r1 = length( P - c1*size) - size/4.25;
    float r2 = length( P - c2*size) - size/4.25;
    float r3 = length( P - c3*size) - size/4.25;
    float r4 =  min(min(r1,r2),r3);

    // Root (2 circles and 2 planes)
    const vec2 c4 = vec2(+0.65, 0.125);
    const vec2 c5 = vec2(-0.65, 0.125);
    float r5 = length(P-c4*size) - size/1.6;
    float r6 = length(P-c5*size) - size/1.6;
    float r7 = P.y - 0.5*size;
    float r8 = 0.2*size - P.y;
    float r9 = max(-min(r5,r6), max(r7,r8));

    return min(r4,r9);
}

// --- chevron
float chevron(vec2 P, float size)
{
    float x = 1/SQRT_2 * (P.x - P.y);
    float y = 1/SQRT_2 * (P.x + P.y);
    float r1 = max(abs(x),        abs(y))        - size/3;
    float r2 = max(abs(x-size/3), abs(y-size/3)) - size/3;
    return max(r1,-r2);
}

// --- clover
float clover(vec2 P, float size)
{
    const float t1 = -PI/2;
    const vec2  c1 = 0.25*vec2(cos(t1),sin(t1));
    const float t2 = t1+2*PI/3;
    const vec2  c2 = 0.25*vec2(cos(t2),sin(t2));
    const float t3 = t2+2*PI/3;
    const vec2  c3 = 0.25*vec2(cos(t3),sin(t3));

    float r1 = length( P - c1*size) - size/3.5;
    float r2 = length( P - c2*size) - size/3.5;
    float r3 = length( P - c3*size) - size/3.5;
    return min(min(r1,r2),r3);
}

// --- ring
float ring(vec2 P, float size)
{
    float r1 = length(P) - size/2;
    float r2 = length(P) - size/4;
    return max(r1,-r2);
}

// --- tag
float tag(vec2 P, float size)
{
    float r1 = max(abs(P.x)- size/2, abs(P.y)- size/6);
    float r2 = abs(P.x-size/1.5)+abs(P.y)-size;
    return max(r1,.75*r2);
}

// --- cross
float cross(vec2 P, float size)
{
    float x = SQRT_2/2 * (P.x - P.y);
    float y = SQRT_2/2 * (P.x + P.y);
    float r1 = max(abs(x - size/3), abs(x + size/3));
    float r2 = max(abs(y - size/3), abs(y + size/3));
    float r3 = max(abs(x), abs(y));
    float r = max(min(r1,r2),r3);
    r -= size/2;
    return r;
}

// --- asterisk
float asterisk(vec2 P, float size)
{
    float x = SQRT_2/2 * (P.x - P.y);
    float y = SQRT_2/2 * (P.x + P.y);
    float r1 = max(abs(x)- size/2, abs(y)- size/10);
    float r2 = max(abs(y)- size/2, abs(x)- size/10);
    float r3 = max(abs(P.x)- size/2, abs(P.y)- size/10);
    float r4 = max(abs(P.y)- size/2, abs(P.x)- size/10);
    return min( min(r1,r2), min(r3,r4));
}

// --- infinity
float infinity(vec2 P, float size)
{
    const vec2 c1 = vec2(+0.2125, 0.00);
    const vec2 c2 = vec2(-0.2125, 0.00);
    float r1 = length(P-c1*size) - size/3.5;
    float r2 = length(P-c1*size) - size/7.5;
    float r3 = length(P-c2*size) - size/3.5;
    float r4 = length(P-c2*size) - size/7.5;
    return min( max(r1,-r2), max(r3,-r4));
}

// --- pin
float pin(vec2 P, float size)
{
    vec2 c1 = vec2(0.0,-0.15)*size;
    float r1 = length(P-c1)-size/2.675;
    vec2 c2 = vec2(+1.49,-0.80)*size;
    float r2 = length(P-c2) - 2.*size;
    vec2 c3 = vec2(-1.49,-0.80)*size;
    float r3 = length(P-c3) - 2.*size;
    float r4 = length(P-c1)-size/5;
    return max( min(r1,max(max(r2,r3),-P.y)), -r4);
}

// --- arrow
float marker(vec2 P, float size)
{
    float r1 = abs(P.x) + abs(P.y) - size/2;
    float r2 = max(abs(P.x+size/2), abs(P.y)) - size/2;
    float r3 = max(abs(P.x-size/6)-size/4, abs(P.y)- size/4);
    return min(r3,max(.75*r1,r2));
}

// --- ellipse
// Created by Inigo Quilez - iq/2013
// License Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License.
float ellipse(vec2 P, float size)
{
/*
    // Alternate version (approximation)
    float a = 1.0;
    float b = 3.0;
    float r = 0.9;
    float f = length( p*vec2(a,b) );
    f = length( p*vec2(a,b) );
    f = f*(f-r)/length( p*vec2(a*a,b*b) );
    return f;
*/

    vec2 ab = vec2(size/3.0, size/2.0);
    vec2 p = abs( P );
    if( p.x > p.y ){
        p = p.yx;
        ab = ab.yx;
    }
    float l = ab.y*ab.y - ab.x*ab.x;
    float m = ab.x*p.x/l;
    float n = ab.y*p.y/l;
    float m2 = m*m;
    float n2 = n*n;

    float c = (m2 + n2 - 1.0)/3.0;
    float c3 = c*c*c;

    float q = c3 + m2*n2*2.0;
    float d = c3 + m2*n2;
    float g = m + m*n2;

    float co;

    if(d < 0.0)
    {
        float p = acos(q/c3)/3.0;
        float s = cos(p);
        float t = sin(p)*sqrt(3.0);
        float rx = sqrt( -c*(s + t + 2.0) + m2 );
        float ry = sqrt( -c*(s - t + 2.0) + m2 );
        co = ( ry + sign(l)*rx + abs(g)/(rx*ry) - m)/2.0;
    }
    else
    {
        float h = 2.0*m*n*sqrt( d );
        float s = sign(q+h)*pow( abs(q+h), 1.0/3.0 );
        float u = sign(q-h)*pow( abs(q-h), 1.0/3.0 );
        float rx = -s - u - c*4.0 + 2.0*m2;
        float ry = (s - u)*sqrt(3.0);
        float rm = sqrt( rx*rx + ry*ry );
        float p = ry/sqrt(rm-rx);
        co = (p + 2.0*g/rm - m)/2.0;
    }

    float si = sqrt(1.0 - co*co);
    vec2 closestPoint = vec2(ab.x*co, ab.y*si);
    return length(closestPoint - p ) * sign(p.y-closestPoint.y);
}
