// ----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
// Distributed under the (new) BSD License.
// ----------------------------------------------------------------------------
/*
  Linear scales are the most common scale, and a good default choice to map a
  continuous input domain to a continuous output range. The mapping is linear
  in that the output range value y can be expressed as a linear function of the
  input domain value x: y = mx + b. The input domain is typically a dimension
  of the data that you want to visualize, such as the height of students
  (measured in meters) in a sample population. The output range is typically a
  dimension of the desired output visualization, such as the height of bars
  (measured in pixels) in a histogram.
*/
uniform int  linear_scale_clamp;
uniform vec4 linear_scale_x;
uniform vec4 linear_scale_y;
uniform vec4 linear_scale_z;


float linear_scale_forward(float value)
{
    float domain_inf = linear_scale_x.x;
    float domain_sup = linear_scale_x.y;
    float range_inf  = linear_scale_x.z;
    float range_sup  = linear_scale_x.w;

    float t = (value - domain_inf) /(domain_sup - domain_inf);
    if (linear_scale_clamp > 0) t = clamp(t,0.0,1.0);
    return range_inf + t*(range_sup - range_inf);
}

vec2 linear_scale_forward(vec2 value)
{
    vec2 domain_inf = vec2(linear_scale_x.x, linear_scale_y.x);
    vec2 domain_sup = vec2(linear_scale_x.y, linear_scale_y.y);
    vec2 range_inf  = vec2(linear_scale_x.z, linear_scale_y.z);
    vec2 range_sup  = vec2(linear_scale_x.w, linear_scale_y.w);

    vec2 t = (value - domain_inf) /(domain_sup - domain_inf);
    if (linear_scale_clamp > 0)  t = clamp(t,0.0,1.0);
    return range_inf + t*(range_sup - range_inf);
}

vec3 linear_scale_forward(vec3 value)
{
    vec3 domain_inf = vec3(linear_scale_x.x, linear_scale_y.x, linear_scale_z.x);
    vec3 domain_sup = vec3(linear_scale_x.y, linear_scale_y.y, linear_scale_z.y);
    vec3 range_inf  = vec3(linear_scale_x.z, linear_scale_y.z, linear_scale_z.z);
    vec3 range_sup  = vec3(linear_scale_x.w, linear_scale_y.w, linear_scale_z.w);

    vec3 t = (value - domain_inf) /(domain_sup - domain_inf);
    if (linear_scale_clamp > 0) t = clamp(t,0.0,1.0);
    return range_inf + t*(range_sup - range_inf);
}
