#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import numpy as np
import glumpy
import glumpy.gl as gl
import glumpy.glm as glm
import glumpy.app as app
import glumpy.gloo as gloo

from font import Font


def label(text, font, anchor_x='right', anchor_y='baseline'):

    n = len(text) - text.count('\n')
    indices = np.zeros((n,6), dtype=np.uint32)
    vertices = np.zeros((n,4), dtype= [('position', np.float32, 2),
                                       ('texcoord', np.float32, 2)])
    # Current line start index
    start = 0
    # Pen position
    pen = [0,0]
    # Previous glyph
    prev = None
    # Lines (as start/end index and width (pixels)
    lines = []
    # Maximum text width and total height
    text_width, text_height = 0, 0

    index = 0
    for charcode in text:

        # Line feed
        if charcode == '\n':
            prev = None
            lines.append( ((start, index), pen[0]) )
            start = index
            text_width = max(text_width,pen[0])
            pen[1] -= font.height
            pen[0] = 0
        # Actual glyph
        else:
            glyph = font[charcode]
            kerning = glyph.get_kerning(prev)
            x0 = pen[0] + glyph.offset[0] + kerning
            y0 = pen[1] + glyph.offset[1]
            x1 = x0 + glyph.shape[1]
            y1 = y0 - glyph.shape[0]
            u0, v0, u1, v1 = glyph.texcoords
            vertices[index]['position'] = (x0,y0),(x0,y1),(x1,y1),(x1,y0)
            vertices[index]['texcoord'] = (u0,v0),(u0,v1),(u1,v1),(u1,v0)
            indices[index] = index*4
            indices[index] += 0,1,2, 0,2,3
            pen[0] = pen[0]+glyph.advance[0] + kerning
            pen[1] = pen[1]+glyph.advance[1]
            prev = charcode
            index += 1

    lines.append( ((start, index+1), pen[0]) )
    text_height = (len(lines)-1)*font.height
    text_width = max(text_width,pen[0])


    # Adjusting each line
    for ((start, end), width) in lines:
        if anchor_x == 'right':
            dx = -width/1.0
        elif anchor_x == 'center':
            dx = -width/2.0
        else:
            dx = 0
        vertices[start:end]['position'] += dx,0

    # Adjusting whole label
    if anchor_y == 'top':
        dy = -font.ascender
    elif anchor_y == 'center':
        dy = text_height/2.0 - font.ascender
    elif anchor_y == 'bottom':
        dy = -font.descender + text_height
    else:
        dy = 0
    vertices['position'] += 0, dy

    return vertices.view(gloo.VertexBuffer), indices.view(gloo.IndexBuffer)


window = app.Window(width=700, height=700)

@window.event
def on_draw():
    global theta, dtheta
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    program.draw(gl.GL_TRIANGLES, I)
    theta += dtheta
    model = np.eye(4, dtype=np.float32)
    glm.rotate(model, theta, 0, 0, 1)
    program['model'] = model

@window.event
def on_resize(width, height):
    gl.glViewport(0, 0, width, height)
    program['projection'] = glm.ortho(0, width, 0, height, -1, +1)
    program['translate'] = width//2,height//2

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
    scale = program["scale"][0]
    program["scale"] = min(max(0.01, scale + .01 * dy * scale), 100)

program = gloo.Program("sdf-glyph.vert",
                       ["spatial-filters.frag", "sdf-glyph.frag"], count=4)
font = Font("Vera.ttf")


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

V,I = label(jabberwocky, font, anchor_x = 'center', anchor_y = 'center')
theta, dtheta = 0.0, 0.0
program.bind(V)
program['u_kernel'] = np.load("spatial-filters.npy")
program['atlas_data'] = font.atlas
program['atlas_data'].interpolation = gl.GL_LINEAR
program['atlas_shape'] = font.atlas.shape[1],font.atlas.shape[0]
program['color'] = 0,0,0,1
program['scale'] = 1.0

gl.glClearColor(1.0, 1.0, 1.0, 1.0)
gl.glDisable(gl.GL_DEPTH_TEST)
gl.glEnable(gl.GL_BLEND)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

app.run()
