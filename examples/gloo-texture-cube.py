#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gloo, gl, glm
from glumpy.transforms import Trackball, Position

vertex = """
    attribute vec3 position;
    attribute vec3 texcoord;
    varying vec3 v_texcoord;
    void main()
    {
        gl_Position = <transform(position)>;
        v_texcoord = texcoord;
    }
"""

fragment = """
    uniform samplerCube texture;
    varying vec3 v_texcoord;
    void main()
    {
        gl_FragColor = textureCube(texture, v_texcoord);
    }
"""


window = app.Window(width=512, height=512)

@window.event
def on_draw(dt):
    window.clear()
    program.draw(gl.GL_TRIANGLES, indices)

@window.event
def on_init():
    gl.glEnable(gl.GL_DEPTH_TEST)

vertices = np.array([[1, 1, 1], [-1, 1, 1], [-1, -1, 1], [1, -1, 1],
                     [1, -1, -1], [1, 1, -1], [-1, 1, -1], [-1, -1, -1]])
faces = [vertices[i] for i in [0,1,2,3, 0,3,4,5, 0,5,6,1,
                               1,6,7,2, 7,4,3,2, 4,7,6,5] ]
indices = np.resize(np.array([0,1,2,0,2,3], dtype=np.uint32), 36)
indices += np.repeat(4 * np.arange(6, dtype=np.uint32), 6)
indices = indices.view(gloo.IndexBuffer)
texture = np.zeros((6,32,32,4),dtype=np.float32).view(gloo.TextureCube)


program = gloo.Program(vertex, fragment, count=24)
program['position'] = faces
program['texcoord'] = faces
program['texture'] = texture
program['transform'] = Trackball(Position())

texture[0] = 1,0,0,1
texture[1] = 0,1,0,1
texture[2] = 0,0,1,1
texture[3] = 1,1,0,1
texture[4] = 0,1,1,1
texture[5] = 1,1,1,1

window.attach(program["transform"])
app.run()
