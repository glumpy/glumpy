# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gl, gloo, data, library
from glumpy.geometry import primitives
from glumpy.transforms import Trackball

vertex = """
#include "misc/spatial-filters.frag"

uniform float height;
uniform sampler2D data;
uniform vec2 data_shape;
attribute vec3 position;
attribute vec2 texcoord;

varying vec3 v_position;
varying vec2 v_texcoord;
void main()
{
    float z = height*Bicubic(data, data_shape, texcoord).r;
    gl_Position = <transform>;
    v_texcoord = texcoord;
    v_position = vec3(position.xy, z);
}
"""

fragment = """
#include "misc/spatial-filters.frag"

uniform mat4 model;
uniform mat4 view;
uniform mat4 normal;
uniform sampler2D texture;
uniform float height;
uniform vec4 color;

uniform sampler2D data;
uniform vec2 data_shape;
uniform vec3 light_color[3];
uniform vec3 light_position[3];

varying vec3 v_position;
varying vec2 v_texcoord;

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
    mat4 model = <transform.trackball_model>;

    // Extract data value
    float value = Bicubic(data, data_shape, v_texcoord).r;

    // Compute surface normal using neighbour values
    float hx0 = height*Bicubic(data, data_shape, v_texcoord+vec2(+1,0)/data_shape).r;
    float hx1 = height*Bicubic(data, data_shape, v_texcoord+vec2(-1,0)/data_shape).r;
    float hy0 = height*Bicubic(data, data_shape, v_texcoord+vec2(0,+1)/data_shape).r;
    float hy1 = height*Bicubic(data, data_shape, v_texcoord+vec2(0,-1)/data_shape).r;
    vec3 dx = vec3(2.0/data_shape.x,0.0,hx0-hx1);
    vec3 dy = vec3(0.0,2.0/data_shape.y,hy0-hy1);
    vec3 v_normal = normalize(cross(dx,dy));

    // Map value to rgb color
    float c = 0.6 + 0.4*texture2D(texture, v_texcoord).r;
    vec4 l1 = vec4(light_color[0] * lighting(v_normal, light_position[0]), 1);
    vec4 l2 = vec4(light_color[1] * lighting(v_normal, light_position[1]), 1);
    vec4 l3 = vec4(light_color[2] * lighting(v_normal, light_position[2]), 1);

    gl_FragColor = color * vec4(c,c,c,1) * (0.5 + 0.5*(l1+l2+l3));
} """



window = app.Window(1200, 800, color = (1,1,1,1))



@window.event
def on_draw(dt):
    global phi, theta, time

    time += dt
    window.clear()

    surface['data']

    gl.glDisable(gl.GL_BLEND)
    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glEnable(gl.GL_POLYGON_OFFSET_FILL)
    surface["color"] = 1,1,1,1
    surface.draw(gl.GL_TRIANGLES, s_indices)

    gl.glDisable(gl.GL_POLYGON_OFFSET_FILL)
    gl.glEnable(gl.GL_BLEND)
    gl.glDepthMask(gl.GL_FALSE)
    surface["color"] = 0,0,0,1
    surface.draw(gl.GL_LINE_LOOP, b_indices)
    gl.glDepthMask(gl.GL_TRUE)

    model = surface['transform']['model'].reshape(4,4)
    view  = surface['transform']['view'].reshape(4,4)
    surface['view']  = view
    surface['model'] = model
    surface['normal'] = np.array(np.matrix(np.dot(view, model)).I.T)
    # surface["height"] = 0.75*np.cos(time/5.0)


@window.event
def on_init():
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
    gl.glPolygonOffset(1, 1)
    gl.glEnable(gl.GL_LINE_SMOOTH)
    gl.glLineWidth(2.5)


n = 64
surface = gloo.Program(vertex, fragment)
vertices, s_indices = primitives.plane(2.0, n=n)
surface.bind(vertices)

I = []
for i in range(n): I.append(i)
for i in range(1,n): I.append(n-1+i*n)
for i in range(n-1): I.append(n*n-1-i)
for i in range(n-1): I.append(n*(n-1) - i*n)
b_indices = np.array(I, dtype=np.uint32).view(gloo.IndexBuffer)


def func3(x,y):
    return (1-x/2+x**5+y**3)*np.exp(-x**2-y**2)
x = np.linspace(-2.0, 2.0, 32).astype(np.float32)
y = np.linspace(-2.0, 2.0, 32).astype(np.float32)
X,Y = np.meshgrid(x, y)
Z = func3(X,Y)

surface['data'] = (Z-Z.min())/(Z.max() - Z.min())
surface['data'].interpolation = gl.GL_NEAREST
surface['data_shape'] = Z.shape[1], Z.shape[0]
surface['u_kernel'] = data.get("spatial-filters.npy")
surface['u_kernel'].interpolation = gl.GL_LINEAR
surface['texture'] = data.checkerboard(32,24)

transform = Trackball("vec4(position.xy, z, 1.0)")
surface['transform'] = transform
window.attach(transform)

T = (Z-Z.min())/(Z.max() - Z.min())

surface['height'] = 0.75
surface["light_position[0]"] = 3, 0, 0+5
surface["light_position[1]"] = 0, 3, 0+5
surface["light_position[2]"] = -3, -3, +5
surface["light_color[0]"]    = 1, 0, 0
surface["light_color[1]"]    = 0, 1, 0
surface["light_color[2]"]    = 0, 0, 1
phi, theta = -45, 0
time = 0

app.run()
