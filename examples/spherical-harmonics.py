# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from scipy.special import sph_harm
from glumpy import app, gl, gloo, transforms


def sphere(radius=1.0, slices=256, stacks=256):
    vtype = [('theta', np.float32, 1),
             ('phi', np.float32, 1)]
    slices += 1
    stacks += 1
    n = slices*stacks
    vertices = np.zeros(n, dtype=vtype)
    vertices["theta"] = np.repeat(np.linspace(0, np.pi, stacks, endpoint=True), slices)
    vertices["phi"] = np.tile(np.linspace(0, 2 * np.pi, slices, endpoint=True), stacks)
    indices = []
    for i in range(stacks-1):
        for j in range(slices-1):
            indices.append(i*(slices) + j        )
            indices.append(i*(slices) + j+1      )
            indices.append(i*(slices) + j+slices+1)
            indices.append(i*(slices) + j+slices  )
            indices.append(i*(slices) + j+slices+1)
            indices.append(i*(slices) + j        )
    indices = np.array(indices, dtype=np.uint32)
    return vertices.view(gloo.VertexBuffer), indices.view(gloo.IndexBuffer)


vertex = """
float harmonic(float theta, float phi, float m[8])
{
    return pow(sin(m[0]*phi),m[1]) + pow(sin(m[4]*theta),m[5]) +
           pow(cos(m[2]*phi),m[3]) + pow(cos(m[6]*theta),m[7]);
}

uniform float time;
uniform float m1[8];
uniform float m2[8];

attribute float phi;
attribute float theta;
varying float v_theta;
varying float v_phi;
varying vec3 v_position;

void main()
{
    float radius, x, y, z;

    v_phi = phi;
    v_theta = theta;

    radius = 1.0 + 0.15*(harmonic(theta,phi,m1));
    x = sin(theta) * sin(phi) * radius;
    y = sin(theta) * cos(phi) * radius;
    z = cos(theta) * radius;
    vec3 position1 = vec3(x,y,z);

    radius = 1.0 + 0.15*(harmonic(theta,phi,m2));
    x = sin(theta) * sin(phi) * radius;
    y = sin(theta) * cos(phi) * radius;
    z = cos(theta) * radius;
    vec3 position2 = vec3(x,y,z);

    float t = (1.0+cos(time))/2.0;
    vec4 position = vec4(mix(position1, position2,t), 1.0);
    v_position = position.xyz;

    gl_Position = <transform(position)>;
}
"""

fragment = """
float segment(float edge0, float edge1, float x)
{
    return step(edge0,x) * (1.0-step(edge1,x));
}
vec3 ice(float t)
{
    return vec3(t, t, 1.0);
}
vec3 fire(float t) {
    return mix(mix(vec3(1,1,1),vec3(1,1,0),t),mix(vec3(1,1,0),vec3(1,0,0),t*t),t);
}
vec3 ice_and_fire(float t)
{
    return segment(0.0,0.5,t)*ice(2.0*(t-0.0)) + segment(0.5,1.0,t)*fire(2.0*(t-0.5));
}

float harmonic(float theta, float phi, float m[8])
{
    return pow(sin(m[0]*phi),m[1]) + pow(sin(m[4]*theta),m[5]) +
           pow(cos(m[2]*phi),m[3]) + pow(cos(m[6]*theta),m[7]);
}

uniform float time;
uniform float m1[8];
uniform float m2[8];

varying vec3 v_position;
varying vec3 v_normal;
varying float v_phi;
varying float v_theta;
void main()
{
    float t1 = (harmonic(v_theta, v_phi, m1)) / 4.0;
    float t2 = (harmonic(v_theta, v_phi, m2)) / 4.0;
    float t = (1.0+cos(time))/2.0;
    t = mix(t1,t2,t);

    vec4 bg_color = vec4(ice_and_fire(clamp(t,0,1)),1.0);
    vec4 fg_color = vec4(0,0,0,1);

    // Trace contour
    float value = length(v_position);
    float levels = 16.0;
    float antialias = 1.0;
    float linewidth = 1.0 + antialias;
    float v  = levels*value - 0.5;
    float dv = linewidth/2.0 * fwidth(v);
    float f = abs(fract(v) - 0.5);
    float d = smoothstep(-dv,+dv,f);
    t = linewidth/2.0 - antialias;

    d = abs(d)*linewidth/2.0 - t;
    if( d < 0.0 ) {
         gl_FragColor = bg_color;
    } else  {
        d /= antialias;
        gl_FragColor = mix(fg_color,bg_color,d);
    }


}
"""

window = app.Window(width=1024, height=1024, color=(.3,.3,.3,1))

@window.event
def on_draw(dt):
    global time
    time += dt

    window.clear()
    program["time"] = time
    program.draw(gl.GL_TRIANGLES, faces)

    # trackball.phi = trackball.phi + 0.13
    # trackball.theta = trackball.theta + 0.11

    if (abs(time - np.pi)) < dt:
        values = np.random.randint(0,7,8)
        keys   = ["m2[0]","m2[1]","m2[2]","m2[3]","m2[4]","m2[5]","m2[6]","m2[7]"]
        for key,value in zip(keys, values):
            program[key] = value

    elif (abs(time - 2*np.pi)) < dt:
        values = np.random.randint(0,7,8)
        keys   = ["m1[0]","m1[1]","m1[2]","m1[3]","m1[4]","m1[5]","m1[6]","m1[7]"]
        for key,value in zip(keys, values):
            program[key] = value
        time = 0

@window.event
def on_init():
    gl.glEnable(gl.GL_DEPTH_TEST)

time = 0
vertices, faces = sphere()
program = gloo.Program(vertex, fragment)
trackball = transforms.Trackball()
program["transform"] = trackball()
program.bind(vertices)

values = np.random.randint(0,7,8)
keys   = ["m1[0]","m1[1]","m1[2]","m1[3]","m1[4]","m1[5]","m1[6]","m1[7]"]
for key,value in zip(keys, values):
    program[key] = value

values = np.random.randint(0,7,8)
keys   = ["m2[0]","m2[1]","m2[2]","m2[3]","m2[4]","m2[5]","m2[6]","m2[7]"]
for key,value in zip(keys, values):
    program[key] = value

trackball.zoom = 30
window.attach(program["transform"])
app.run()
