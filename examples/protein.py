# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
from glumpy import app, gloo, gl, data
from glumpy.transforms import Position, Trackball
from glumpy.graphics.filter import Filter

vertex = """
uniform vec3 light_position;

attribute vec3 position;
attribute vec3 color;
attribute float radius;

varying float v_size;
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
    v_size = 512.0 * p.x / p.w;
    gl_PointSize = v_size + 5.0;
}
"""

fragment = """
#include "antialias/outline.glsl"


varying float v_size;
varying vec3 v_color;
varying float v_radius;
varying vec4 v_eye_position;
varying vec3 v_light_direction;

void main()
{
    vec2 P = gl_PointCoord.xy - vec2(0.5,0.5);
    float point_size = v_size  + 5.0;
    float distance = length(P*point_size) - v_size/2;

    vec2 texcoord = gl_PointCoord* 2.0 - vec2(1.0);
    float x = texcoord.x;
    float y = texcoord.y;
    float d = 1.0 - x*x - y*y;

    if (d <= 0.0) discard;

    float z = sqrt(d);
    vec4 pos = v_eye_position;
    pos.z += v_radius*z;
    vec3 pos2 = pos.xyz;

    pos = <transform.trackball_projection> * pos;
    gl_FragDepth = 0.5*(pos.z / pos.w)+0.5;
    vec3 normal = vec3(x,y,z);
    float diffuse = clamp(dot(normal, v_light_direction), 0.0, 1.0);

    vec4 color = vec4((0.5 + 0.5*diffuse)*v_color, 1.0);
    gl_FragColor = outline(distance, 1.0, 1.0, vec4(0,0,0,1), color);
    // gl_FragColor = color;
}
"""

window = app.Window(width=800, height=800, color=(1,1,1,1))

protein = gloo.Program(vertex, fragment)
protein['light_position'] = 0., 0., 2.
protein["transform"] = Trackball(Position())
protein.bind(data.get("protein.npy").view(gloo.VertexBuffer))
protein['color'] *= .25
protein['color'] += .75

@window.event
def on_draw(dt):
    window.clear()
    protein.draw(gl.GL_POINTS)

@window.event
def on_init():
    gl.glEnable(gl.GL_DEPTH_TEST)

window.attach(protein["transform"])
app.run()
