# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
from glumpy import app
from glumpy.graphics.text import FontManager
from glumpy.graphics.collections import GlyphCollection
from glumpy.transforms import Position, OrthographicProjection, Viewport

window = app.Window(width=1200, height=800, color=(1,1,1,1))

@window.event
def on_draw(dt):
    window.clear()
    labels.draw()


labels = GlyphCollection(transform=OrthographicProjection(Position()))
regular = FontManager.get("OpenSans-Regular.ttf")
text = "The quick brown fox jumps over the lazy dog"
x,y,z = 2,window.height,0

for i in range(6,54,2):
    scale = i/48.0
    y -= i*1.1
    labels.append(text, regular, origin = (x,y,z), scale=scale, anchor_x="left")


window.attach(labels["transform"])
window.attach(labels["viewport"])
app.run()
