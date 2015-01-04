// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------
/*
  Power scales are similar to linear scales, except there's an exponential
  transform that is applied to the input domain value before the output range
  value is computed. The mapping to the output range value y can be expressed
  as a function of the input domain value x: y = mx^k + b, where k is the
  exponent value. Power scales also support negative values, in which case the
  input value is multiplied by -1, and the resulting output value is also
  multiplied by -1.
*/
uniform int  power_scale_clamp;
uniform vec2 power_scale_range;
uniform vec2 power_scale_domain;
uniform float power_scale_exponent;

float power_scale_forward(float value)
{
    vec2 domain = power_scale_domain;
    vec2 range = power_scale_range;
    float exponent = power_scale_exponent;

    float v = pow(abs(value), exponent);
    float t = (v - domain.x) /(domain.y - domain.x);
    if (power_scale_clamp > 0) t = clamp(t,0.0,1.0);

    return sign(value) * (range.x + t*(range.y - range.x));
}

vec2 power_scale_forward(vec2 value)
{
    vec2 domain = power_scale_domain;
    vec2 range = power_scale_range;
    float exponent = power_scale_exponent;

    vec2 v = pow(abs(value), vec2(exponent));
    vec2 t = (v - domain.x) /(domain.y - domain.x);
    if (power_scale_clamp > 0) t = clamp(t,0.0,1.0);

    return sign(value) * (range.x + t*(range.y - range.x));
}

vec3 power_scale_forward(vec3 value)
{
    vec2 domain = power_scale_domain;
    vec2 range = power_scale_range;
    float exponent = power_scale_exponent;

    vec3 v = pow(abs(value), vec3(exponent));
    vec3 t = (v - domain.x) /(domain.y - domain.x);
    if (power_scale_clamp > 0) t = clamp(t,0.0,1.0);

    return sign(value) * (range.x + t*(range.y - range.x));
}
