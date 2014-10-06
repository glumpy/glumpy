#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import numpy as np
import glumpy as gp
import glumpy.gl as gl
import glumpy.glm as glm


from font import Font


window = gp.Window(width=700, height=700)

@window.event
def on_draw(dt):
    global theta, dtheta
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    C.draw()
    theta += dtheta
    model = np.eye(4, dtype=np.float32)
    glm.rotate(model, theta, 0, 0, 1)
    C['model'] = model

@window.event
def on_resize(width, height):
    gl.glViewport(0, 0, width, height)
    C['projection'] = glm.ortho(0, width, 0, height, -1, +1)
    C['translate'] = width//2,height//2

@window.event
def on_key_press(key, modifier):
    global theta, dtheta
    if key == 32:
        if dtheta:
            dtheta = 0.00
        else:
            dtheta = 0.25

@window.event
def on_mouse_scroll(x, y, dx, dy):
    scale = C["scale"][0]
    C["scale"] = min(max(0.01, scale + .01 * dy * scale), 100)


jabberwocky = (
"`Twas brillig, and the slithy toves\n"
"  Did gyre and gimble in the wabe:\n"
"All mimsy were the borogoves,\n"
"  And the mome raths outgrabe.\n"
"\n"
"\"Beware the Jabberwock, my son!\n"
"  The jaws that bite, the claws that catch!\n"
"Beware the Jubjub bird, and shun\n"
"  The frumious Bandersnatch!\"\n"
"He took his vorpal sword in hand:\n"
"  Long time the manxome foe he sought --\n"
"So rested he by the Tumtum tree,\n"
"  And stood awhile in thought.\n"
"And, as in uffish thought he stood,\n"
"  The Jabberwock, with eyes of flame,\n"
"Came whiffling through the tulgey wood,\n"
"  And burbled as it came!\n"
"One, two! One, two! And through and through\n"
"  The vorpal blade went snicker-snack!\n"
"He left it dead, and with its head\n"
"  He went galumphing back.\n"
"\"And, has thou slain the Jabberwock?\n"
"  Come to my arms, my beamish boy!\n"
"O frabjous day! Callooh! Callay!'\n"
"  He chortled in his joy.\n"
"\n"
"`Twas brillig, and the slithy toves\n"
"  Did gyre and gimble in the wabe;\n"
"All mimsy were the borogoves,\n"
"  And the mome raths outgrabe.\n" )

font = Font("OpenSans-Regular.ttf")

C = gp.GlyphCollection()
C.append(jabberwocky, font)

theta,dtheta = 0,0
C['u_kernel'] = np.load("spatial-filters.npy")
C['atlas_data'] = font.atlas
C['atlas_data'].interpolation = gl.GL_LINEAR
C['atlas_shape'] = font.atlas.shape[1],font.atlas.shape[0]
C['color'] = 0,0,0,1
C['scale'] = 1.0

gl.glClearColor(1.0, 1.0, 1.0, 1.0)
gl.glDisable(gl.GL_DEPTH_TEST)
gl.glEnable(gl.GL_BLEND)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
gp.run()
