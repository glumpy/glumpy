// -----------------------------------------------------------------------------
// Copyright (c) 2014, Nicolas P. Rougier
// Distributed under the (new) BSD License. See LICENSE.txt for more info.
// -----------------------------------------------------------------------------
uniform float theta;

vec4 forward(vec4 position)
{
  float sin_theta = sin(theta);
  float cos_theta = cos(theta);

  float x = position.x * cos_theta - position.y * sin_theta;
  float y = position.x * sin_theta + position.y * cos_theta;

  return vec4(x, y, position.z, 1.0);
}

vec4 inverse(vec4 position)
{
  float sin_theta = sin(-theta);
  float cos_theta = cos(-theta);

  float x = position.x * cos_theta - position.y * sin_theta;
  float y = position.x * sin_theta + position.y * cos_theta;

  return vec4(x, y, position.z, 1.0);
}
