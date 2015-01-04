// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------
/*
  Log scales are similar to linear scales, except there's a logarithmic
  transform that is applied to the input domain value before the output range
  value is computed. The mapping to the output range value y can be expressed
  as a function of the input domain value x: y = m log(x) + b.

  As log(0) is negative infinity, a log scale must have either an
  exclusively-positive or exclusively-negative domain; the domain must not
  include or cross zero. A log scale with a positive domain has a well-defined
  behavior for positive values, and a log scale with a negative domain has a
  well-defined behavior for negative values (the input value is multiplied by
  -1, and the resulting output value is also multiplied by -1). The behavior of
  the scale is undefined if you pass a negative value to a log scale with a
  positive domain or vice versa.
*/

uniform int  log_scale_clamp;
uniform vec3 log_scale_base;
uniform vec4 log_scale_x;
uniform vec4 log_scale_y;
uniform vec4 log_scale_z;


float log_scale_forward(float value)
{
    float domain_inf = log_scale_x.x;
    float domain_sup = log_scale_x.y;
    float range_inf  = log_scale_x.z;
    float range_sup  = log_scale_x.w;
    float base       = log_scale_base.x;

    float v = log(value) / log(base);

    float t = (v - domain_inf) /(domain_sup - domain_inf);
    if (log_scale_clamp > 0) t = clamp(t,0.0,1.0);
    return sign(value) * (range_inf + t*(range_sup - range_inf));
}

vec2 log_scale_forward(vec2 value)
{
    vec2 domain_inf = vec2(log_scale_x.x, log_scale_y.x);
    vec2 domain_sup = vec2(log_scale_x.y, log_scale_y.y);
    vec2 range_inf  = vec2(log_scale_x.z, log_scale_y.z);
    vec2 range_sup  = vec2(log_scale_x.w, log_scale_y.w);
    vec2 base       = log_scale_base.xy;

    vec2 v = log(value) / log(base);

    vec2 t = (v - domain_inf) /(domain_sup - domain_inf);
    if (log_scale_clamp > 0)  t = clamp(t,0.0,1.0);
    return sign(value) * (range_inf + t*(range_sup - range_inf));
}

vec3 log_scale_forward(vec3 value)
{
    vec3 domain_inf = vec3(log_scale_x.x, log_scale_y.x, log_scale_z.x);
    vec3 domain_sup = vec3(log_scale_x.y, log_scale_y.y, log_scale_z.y);
    vec3 range_inf  = vec3(log_scale_x.z, log_scale_y.z, log_scale_z.z);
    vec3 range_sup  = vec3(log_scale_x.w, log_scale_y.w, log_scale_z.w);
    vec3 base       = log_scale_base.xyz;

    vec3 v = log(value) / log(base);

    vec3 t = (v - domain_inf) /(domain_sup - domain_inf);
    if (log_scale_clamp > 0) t = clamp(t,0.0,1.0);
    return sign(value) * (range_inf + t*(range_sup - range_inf));
}
