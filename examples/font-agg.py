# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
from glumpy import app
from glumpy.log import log
from glumpy.graphics.text import FontManager
from glumpy.graphics.collections import GlyphCollection
from glumpy.transforms import Position, OrthographicProjection, Viewport

window = app.Window(width=1200, height=800, color=(1,1,1,1))

@window.event
def on_draw(dt):
    window.clear()
    labels.draw()


labels = GlyphCollection('agg', transform=OrthographicProjection(Position()))
text = "The quick brown fox jumps over the lazy dog"
x,y,z = 2,window.height,0

log.info("Caching texture fonts")
for i in range(6,54,2):
    font = FontManager.get("OpenSans-Regular.ttf", size=i, mode='agg')
    y -= i*1.1
    labels.append(text, font, origin = (x,y,z), anchor_x="left")

window.attach(labels["transform"])
window.attach(labels["viewport"])
app.run()
