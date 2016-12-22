# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
from glumpy import app, gl, gloo, glm, data
from glumpy.graphics.text import FontManager
from glumpy.graphics.collections import GlyphCollection
from glumpy.transforms import Position, OrthographicProjection

window = app.Window(width=512, height=512)

@window.event
def on_draw(dt):
    window.clear()
    label.draw()

x,y,z = 256,256,0
font = FontManager.get("OpenSans-Regular.ttf", 64, mode='agg')
label = GlyphCollection('agg', transform=OrthographicProjection(Position()))
label.append("Hello World !", font,
                   anchor_x = 'center', anchor_y = 'center',
                   origin=(x,y,z), color=(1,1,1,1))

window.attach(label["transform"])

app.run()
