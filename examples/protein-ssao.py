# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gloo, gl, data
from glumpy.graphics.filter import Filter
from glumpy.transforms import Position, Trackball

vertex = """
uniform vec3 light_position;

attribute vec3 position;
attribute vec3 color;
attribute float radius;

varying vec3 v_color;
varying float v_radius;
varying vec4 v_eye_position;
varying vec3 v_light_direction;

void main (void)
{
    v_color = color;
    v_radius = radius;
    v_eye_position = <transform.trackball_view> *
                     <transform.trackball_model> *
                     vec4(position,1.0);
    v_light_direction = normalize(light_position);
    gl_Position = <transform(position)>;
    // stackoverflow.com/questions/8608844/...
    //  ... resizing-point-sprites-based-on-distance-from-the-camera
    vec4 p = <transform.trackball_projection> *
             vec4(radius, radius, v_eye_position.z, v_eye_position.w);
    gl_PointSize = 512.0 * p.x / p.w;
}
"""

fragment = """
uniform int record;
uniform sampler2D colors;
uniform sampler2D normals;

varying vec3 v_color;
varying float v_radius;
varying vec4 v_eye_position;
varying vec3 v_light_direction;

void main()
{
    vec2 texcoord = gl_PointCoord*2.0 - vec2(1.0);
    float x = texcoord.x;
    float y = texcoord.y;
    float d = 1.0 - x*x - y*y;
    if (d <= 0.0) discard;

    float z = sqrt(d);
    vec4 pos = v_eye_position;
    pos.z += v_radius*z;
    vec3 pos2 = pos.xyz;
    pos = <transform.trackball_projection> * pos;

    float depth = 0.5*(pos.z / pos.w)+0.5;
    vec3 normal = normalize(vec3(x,y,z));

    float diffuse = clamp(dot(normal, v_light_direction), 0.0, 1.0);
    vec3 color = (0.25 + 0.75*diffuse) * (0.75 + 0.25*v_color);

    gl_FragDepth = depth;
    // gl_FragColor = vec4(normal,depth);
    gl_FragData[0] = vec4(color,0.0);
    gl_FragData[1] = vec4(normal,depth);
}
"""

ssao_vertex = """
attribute vec2 position;
varying vec2 v_texcoord;
void main(void)
{
    gl_Position = vec4(2*position-1,0,1);
    v_texcoord = position;
}"""

ssao_fragment = """
uniform sampler2D noise;
uniform sampler2D colors;
uniform sampler2D normals;

uniform float base;
uniform float radius;
uniform float falloff;
uniform float strength;

varying vec2 v_texcoord;

void main(void)
{
  // Samples count
  const int samples = 16;

  // Random vectors inside a unit sphere
  const vec3 sample_kernel[samples] = vec3[](
      vec3( 0.5381, 0.1856,-0.4319), vec3( 0.1379, 0.2486, 0.4430),
      vec3( 0.3371, 0.5679,-0.0057), vec3(-0.6999,-0.0451,-0.0019),
      vec3( 0.0689,-0.1598,-0.8547), vec3( 0.0560, 0.0069,-0.1843),
      vec3(-0.0146, 0.1402, 0.0762), vec3( 0.0100,-0.1924,-0.0344),
      vec3(-0.3577,-0.5301,-0.4358), vec3(-0.3169, 0.1063, 0.0158),
      vec3( 0.0103,-0.5869, 0.0046), vec3(-0.0897,-0.4940, 0.3287),
      vec3( 0.7119,-0.0154,-0.0918), vec3(-0.0533, 0.0596,-0.5411),
      vec3( 0.0352,-0.0631, 0.5460), vec3(-0.4776, 0.2847,-0.0271) );


   // grab a normal for reflecting the sample rays later on
   vec3 fres = normalize(texture2D(noise,v_texcoord).xyz*2.0 - 1.0);

   vec4 sample = texture2D(normals, v_texcoord);
   vec3 color  = texture2D(colors, v_texcoord).xyz;

   vec3 normal = sample.xyz;
   float depth  = sample.a;

   // current fragment coords in screen space
   vec3 ep = vec3(v_texcoord, depth);

   float bl = 0.0;

   // adjust for the depth ( not shure if this is good..)
   float radD = radius / depth;

   vec3 ray, se, occNorm;
   float occluderDepth, depthDifference, normDiff;

   for(int i=0; i<samples; i++)
   {
      // Get a random vector inside the unit sphere
      ray = radD * reflect(sample_kernel[i], fres);

      // If the ray is outside the hemisphere then change direction
      se = ep + sign(dot(ray,normal) )*ray;

      // Get the depth of the occluder fragment
      vec4 occluderFragment = texture2D(normals,se.xy);

      // get the normal of the occluder fragment
      occNorm = occluderFragment.xyz;

      // if depthDifference is negative = occluder is behind current fragment
      depthDifference = depth - occluderFragment.a;

      // calculate the difference between the normals as a weight
      normDiff = (1.0-dot(occNorm,normal));

      // the falloff equation, starts at falloff and is kind of 1/x^2 falling
      bl += step(falloff,depthDifference)*normDiff*(1.0-smoothstep(falloff,strength,depthDifference));
   }

   // output the result
   float ao = 1.0 - base*bl/16;
   gl_FragColor.rgb = color * ao;
   gl_FragColor.a = 1.0;
}
"""

window = app.Window(width=800, height=800, color=(1,1,1,1))

protein = gloo.Program(vertex, fragment)
protein['light_position'] = 0., 0., 2.
protein["transform"] = Trackball(Position(), znear=2.0, zfar=100.0)
protein.bind(data.get("protein.npy").view(gloo.VertexBuffer))

ssao= gloo.Program(ssao_vertex, ssao_fragment, count=4)
ssao['position']= [(0,0), (0,1), (1,0), (1,1)]
ssao['base']    = 1.00
ssao['strength']= 0.20;
ssao['falloff'] = 0.000002;
ssao['radius']  = 0.01;

ssao['normals'] = np.zeros((800,800,4),np.float32).view(gloo.Texture2D)
ssao['normals'].interpolation = gl.GL_LINEAR
ssao['colors'] = np.zeros((800,800,4),np.float32).view(gloo.Texture2D)
ssao['colors'].interpolation = gl.GL_LINEAR
ssao['noise'] = np.random.uniform(0,1,(256,256,3))
ssao['noise'].interpolation = gl.GL_LINEAR

framebuffer = gloo.FrameBuffer(color= [ssao["colors"], ssao["normals"]],
                               depth=gloo.DepthBuffer(800, 800))

@window.event
def on_draw(dt):
    # First pass to record colors, normals and depth
    framebuffer.activate()
    window.clear()
    protein.draw(gl.GL_POINTS)
    framebuffer.deactivate()

    # Actual Screen Space Ambien Occlusion (SSAO)
    window.clear()
    ssao.draw(gl.GL_TRIANGLE_STRIP)

@window.event
def on_init():
    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glDisable(gl.GL_BLEND)

window.attach(protein["transform"])
app.run()
