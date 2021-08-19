# -----------------------------------------------------------------------------
# Copyright (c) 2019 tristanC
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
from glumpy import app, gl, gloo

vertex = """
attribute vec2 position;
void main (void)
{
    gl_Position = vec4(position, 0.0, 1.0);
}
"""

fragment = """
#extension GL_NV_gpu_shader_fp64 : enable
#define AA 2
uniform dvec2 seed;
void main(void)
{
  vec3 col = vec3(0.0);
  for( int m=0; m<AA; m++ )
    for( int n=0; n<AA; n++ ) {
      f64vec2 c = f64vec2(seed);
      f64vec2 z = f64vec2((gl_FragCoord.xy +
                           vec2(float(m), float(n)) / float(AA) - 0.5) /
                          vec2(400., 400.) * 2. - 1.) * .0001;
      int idx;
      for (idx = 0; idx < 256; idx++)
      {
          z = abs(z);
          z = f64vec2(z.x * z.x - z.y * z.y, 2.0 * z.x * z.y ) + c;
          if (dot(z, z) > 2.)
            break;
      }
      col += vec3(idx / 256.);
    }
  gl_FragColor = vec4(col / float(AA * AA), 1.0 );
}
"""

window = app.Window(width=400, height=400)

@window.event
def on_draw(dt):
    window.clear()
    # Small increment that only works with double precision
    seed[0] -= 1e-10
    burningship['seed'] = seed
    burningship.draw(gl.GL_TRIANGLE_STRIP)

burningship = gloo.Program(vertex, fragment, count=4, version=400)
burningship['position'] = [(-1, -1), (-1, +1), (+1, -1), (+1, +1)]
seed = [-1.41323032811858, -0.04230098494239652]
app.run()
