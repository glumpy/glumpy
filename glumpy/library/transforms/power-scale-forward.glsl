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
uniform vec3 power_scale_exponent;
uniform vec4 power_scale_x;
uniform vec4 power_scale_y;
uniform vec4 power_scale_z;


float power_scale_forward(float value)
{
    float domain_inf = power_scale_x.x;
    float domain_sup = power_scale_x.y;
    float range_inf  = power_scale_x.z;
    float range_sup  = power_scale_x.w;
    float exponent   = power_scale_exponent.x;

    float v = pow(abs(value), exponent);
    float t = (v - domain_inf) /(domain_sup - domain_inf);
    if (power_scale_clamp > 0) t = clamp(t,0.0,1.0);
    return sign(value) * (range_inf + t*(range_sup - range_inf));
}

vec2 power_scale_forward(vec2 value)
{
    vec2 domain_inf = vec2(power_scale_x.x, power_scale_y.x);
    vec2 domain_sup = vec2(power_scale_x.y, power_scale_y.y);
    vec2 range_inf  = vec2(power_scale_x.z, power_scale_y.z);
    vec2 range_sup  = vec2(power_scale_x.w, power_scale_y.w);
    vec2 exponent   = power_scale_exponent.xy;

    vec2 v = pow(abs(value), exponent);
    vec2 t = (v - domain_inf) /(domain_sup - domain_inf);
    if (power_scale_clamp > 0)  t = clamp(t,0.0,1.0);
    return sign(value) * (range_inf + t*(range_sup - range_inf));
}

vec3 power_scale_forward(vec3 value)
{
    vec3 domain_inf = vec3(power_scale_x.x, power_scale_y.x, power_scale_z.x);
    vec3 domain_sup = vec3(power_scale_x.y, power_scale_y.y, power_scale_z.y);
    vec3 range_inf  = vec3(power_scale_x.z, power_scale_y.z, power_scale_z.z);
    vec3 range_sup  = vec3(power_scale_x.w, power_scale_y.w, power_scale_z.w);
    vec3 exponent   = power_scale_exponent.xyz;

    vec3 v = pow(abs(value), exponent);
    vec3 t = (v - domain_inf) /(domain_sup - domain_inf);
    if (power_scale_clamp > 0) t = clamp(t,0.0,1.0);
    return sign(value) * (range_inf + t*(range_sup - range_inf));
}
