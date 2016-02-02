# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gl, gloo
from glumpy.geometry import primitives
from glumpy.transforms import Trackball, Position


vertex = """
attribute vec3 position;
attribute vec3 normal;
varying vec3 v_position;
varying vec3 v_normal;
void main()
{
    v_position = position;
    v_normal = normal;
    gl_Position = <transform>;
}
"""

fragment = """
uniform mat4 model;
uniform mat4 view;
uniform mat4 normal;
uniform vec3 light_color[3];
uniform vec3 light_position[3];
varying vec3 v_position;
varying vec3 v_normal;

float lighting(vec3 v_normal, vec3 light_position)
{
    // Calculate normal in world coordinates
    vec3 n = normalize(normal * vec4(v_normal,1.0)).xyz;

    // Calculate the location of this fragment (pixel) in world coordinates
    vec3 position = vec3(view * model * vec4(v_position, 1));

    // Calculate the vector from this pixels surface to the light source
    vec3 surface_to_light = light_position - position;

    // Calculate the cosine of the angle of incidence (brightness)
    float brightness = dot(n, surface_to_light) /
                      (length(surface_to_light) * length(n));
    brightness = max(min(brightness,1.0),0.0);
    return brightness;
}

void main()
{
    vec4 color = vec4(1,1,1,1);
    vec4 l1 = vec4(light_color[0] * lighting(v_normal, light_position[0]), 1);
    vec4 l2 = vec4(light_color[1] * lighting(v_normal, light_position[1]), 1);
    vec4 l3 = vec4(light_color[2] * lighting(v_normal, light_position[2]), 1);
    gl_FragColor = mix(color,(l1+l2+l3), 0.85);
}
"""

window = app.Window(width=1024, height=1024,
                    color=(0.30, 0.30, 0.35, 1.00))

def update():
    model = teapot['transform']['model'].reshape(4,4)
    view  = teapot['transform']['view'].reshape(4,4)
    teapot['view']  = view
    teapot['model'] = model
    teapot['normal'] = np.array(np.matrix(np.dot(view, model)).I.T)
    

@window.event
def on_draw(dt):
    window.clear()
    teapot.draw(gl.GL_TRIANGLES, indices)

@window.event
def on_mouse_drag(x, y, dx, dy, button):
    update()
    
@window.event
def on_init():
    gl.glEnable(gl.GL_DEPTH_TEST)
    update()

vertices, indices = primitives.teapot()
teapot = gloo.Program(vertex, fragment)
teapot.bind(vertices)
trackball = Trackball(Position("position"))
teapot['transform'] = trackball
trackball.theta, trackball.phi, trackball.zoom = 40, 135, 25

teapot["light_position[0]"] = 3, 0, 0+5
teapot["light_position[1]"] = 0, 3, 0+5
teapot["light_position[2]"] = -3, -3, +5
teapot["light_color[0]"]    = 1, 0, 0
teapot["light_color[1]"]    = 0, 1, 0
teapot["light_color[2]"]    = 0, 0, 1

window.attach(teapot['transform'])
app.run()
