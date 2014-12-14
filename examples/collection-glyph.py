#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
from glumpy import app
from glumpy.graphics.text import FontManager
from glumpy.graphics.collection import GlyphCollection
from glumpy.transforms import Position3D, Viewport, Trackball


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

window = app.Window(width=700, height=700, color=(1,1,1,1))

@window.event
def on_draw(dt):
    window.clear()
    C.draw()

transform = Trackball(Position3D()) + Viewport()
window.attach(transform)

C = GlyphCollection(transform=transform)
font = FontManager().get_file("../glumpy/data/fonts/Roboto-Regular.ttf")
C.append(jabberwocky, font)

app.run()
