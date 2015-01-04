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
uniform vec2 log_scale_range;
uniform vec2 log_scale_domain;
uniform float log_scale_base;

float log_scale_forward(float value)
{
    vec2 domain = log_scale_domain;
    vec2 range = log_scale_range;
    float base = log_scale_base;

    float v = log(value) / base;
    float t = (v - domain.x) /(domain.y - domain.x);
    if (log_scale_clamp > 0) t = clamp(t,0.0,1.0);

    return sign(value) * (range.x + t*(range.y - range.x));
}

vec2 log_scale_forward(vec2 value)
{
    vec2 domain = log_scale_domain;
    vec2 range = log_scale_range;
    float base = log_scale_base;

    vec2 v = log(value) / base;
    vec2 t = (v - domain.x) /(domain.y - domain.x);
    if (log_scale_clamp > 0) t = clamp(t,0.0,1.0);

    return sign(value) * (range.x + t*(range.y - range.x));
}

vec3 log_scale_forward(vec3 value)
{
    vec2 domain = log_scale_domain;
    vec2 range = log_scale_range;
    float base = log_scale_base;

    vec3 v = log(value) / base;
    vec3 t = (v - domain.x) /(domain.y - domain.x);
    if (log_scale_clamp > 0) t = clamp(t,0.0,1.0);

    return sign(value) * (range.x + t*(range.y - range.x));
}
