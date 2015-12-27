# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
from glumpy import app, gl, gloo, glm, data, text

window = app.Window(width=512, height=512)

@window.event
def on_draw(dt):
    window.clear()
    label.draw(x=256, y=256, color=(1,1,1,1))

font = text.TextureFont(data.get("OpenSans-Regular.ttf"), 64)
label = text.Label("Hello World !", font,
                   anchor_x = 'center', anchor_y = 'center')
app.run()
