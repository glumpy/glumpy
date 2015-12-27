# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, color, collections
from glumpy.graphics.text import FontManager
from glumpy.transforms import OrthographicProjection, Position, PanZoom, Viewport


window = app.Window(1400,1050, color=(1,1,1,1))

@window.event
def on_draw(dt):
    window.clear()
    quads.draw()
    labels.draw()

@window.event
def on_key_press(key, modifiers):
    if key == app.window.key.SPACE:
        transform.pan = 0.0,0.0
        transform.zoom = 0.165


def add(names, values, xmin, xmax, ymin, ymax, header=None):
    colors = color.Colors(values)
    n = len(colors)
    dy = (ymax-ymin)/n
    for i,y in enumerate(np.linspace(ymin,ymax,n+1)[:-1]):

        quads.append( [(xmin,y,0), (xmin,y+dy,0), (xmax,y+dy,0), (xmax,y,0)],
                      [0,1,2,0,2,3], color = colors[i].rgba)

        r,g,b,a = colors[i].rgba
        gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
        if gray < 0.5:
            c = 1,1,1,1
        else:
            c = 0,0,0,1
        x = xmin + 0.05*(xmax-xmin)
        if header is None:
            y = y+dy/2
        else:
            y = y + 0.15*(ymax-ymin)

        labels.append(names[i].upper(), regular, color=c,
                      origin = (x,y,0), scale = 0.002, direction = (1,0,0),
                      anchor_x = "left", anchor_y = "center")
        labels.append(names[i].upper(), regular, color=c,
                      origin = (x,y,0), scale = 0.002, direction = (1,0,0),
                      anchor_x = "left", anchor_y = "center")
        if header is not None:
            labels.append(header, regular, color=c,
                          origin = (x,ymax - 0.25*(ymax-ymin),0),
                          scale = 0.005, direction = (1,0,0),
                          anchor_x = "left", anchor_y = "center")

        x = xmax - 0.05*(xmax-xmin)
        labels.append(values[i].upper(), regular, color=c,
                      origin = (x,y,0), scale = 0.002, direction = (1,0,0),
                      anchor_x = "right", anchor_y = "center")



transform = PanZoom(OrthographicProjection(Position(),normalize=True),aspect=1)
transform.zoom = 0.165
viewport = Viewport()

quads  = collections.TriangleCollection(transform = transform, viewport=viewport)
labels = collections.GlyphCollection(transform = transform, viewport=viewport)
regular = FontManager.get("OpenSans-Regular.ttf")


x,y = -2.5*2.6,+4
for i,name in enumerate(["Red", "Pink", "Purple",  "Deep Purple", "Indigo", "Blue",
                         "Light Blue", "Cyan", "Teal", "Green", "Light Green", "Lime",
                         "Yellow", "Amber", "Orange", "Deep Orange", "Brown", "Grey"]):
    family = "material:%s" % name
    if i > 0 and (i % 6) == 0:
        y -= 4
        x = -2.5*2.6
    if name not in ["Brown", "Grey"]:
        names  = list(color.get(family).keys())[:-1][::-1]
        values = color.get(family+":*")[:-4][::-1]
    else:
        names  = list(color.get(family).keys())[::-1]
        values = color.get(family+":*")[::-1]
    add(names, values, x-1.25, x+1.25, y-1.000, y+1.000)
    if name not in ["Brown", "Grey"]:
        names  = ["A"+ v for v in list(color.get(family+":accent").keys())[::-1]]
        values = color.get(family+":accent:*")[::-1]
        add(names, values, x-1.25, x+1.25, y-1.850, y-1.050)

    names  = ["500"]
    values = [color.get(family+":500")]
    add(names, values, x-1.25, x+1.25, y+1.050, y+1.850, header=name)
    x += 2.6

window.attach(transform)
window.attach(viewport)

app.run()
