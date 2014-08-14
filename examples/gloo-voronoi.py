#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gl, glm, gloo


vertex = """
uniform mat4 projection;
uniform vec2 iResolution;
attribute vec2 translate;
attribute vec3 position;
attribute vec3 color;
varying vec3 v_color;
void main()
{
    v_color = color;
    gl_Position = projection * vec4(position.xy+translate, position.z ,1.0);
}
"""

fragment = """
varying vec3 v_color;
void main()
{
    gl_FragColor = vec4(v_color.rgb, 1.0);
}
"""

window = app.Window(width=1024, height=1024)

@window.event
def on_draw(dt):
    window.clear()
    cones.draw(gl.GL_TRIANGLES, I)

@window.event
def on_resize(width, height):
    cones['projection'] = glm.ortho(0, width, 0, height, -5, +5000)
    cones['iResolution'] = width, height

@window.event
def on_mouse_motion(x,y,dx,dy):
    C["translate"][0] = x, window.height-y


def makecone(n=32, radius=1024):
    height = radius / np.tan(45 * np.pi / 180.0)
    V = np.zeros((1+n,3))
    V[0] = 0,0,0
    T = np.linspace(0,2*np.pi,n, endpoint=False)
    V[1:,0] = radius*np.cos(T)
    V[1:,1] = radius*np.sin(T)
    V[1:,2] = -height
    I = np.repeat([[0,1,2]], n, axis=0) + np.arange(n).reshape(n,1)
    I[:,0] = 0
    I[-1] = 0,n,1
    return V, I.ravel()


n = 4*512 # number of cones (= number of point)
p = 32  # faces per cones
C = np.zeros((n,1+p), [("translate", np.float32, 2),
                       ("position",  np.float32, 3),
                       ("color",     np.float32, 3)]).view(gloo.VertexBuffer)
I = np.zeros((n,3*p), np.uint32).view(gloo.IndexBuffer)
I += (1+p)*np.arange(n).reshape(n,1)
for i in range(n):
    #x,y = np.random.uniform(0,1024,2)
    x,y = np.random.normal(512,256,2)
    vertices, indices = makecone(p, radius=512)

    if i > 0:
        l = np.random.uniform(0.25,1.00)
        C["color"][i] = l,l,l
    else:
        C["color"][0] = 1,1,0

    C["translate"][i] = x,y
    C["position"][i] = vertices
    I[i] += indices.ravel()
cones = gloo.Program(vertex, fragment)
cones.bind(C)


gl.glEnable(gl.GL_DEPTH_TEST)
app.run()
