#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy.graphics.text import FontManager
from glumpy import app, color, collections, key
from glumpy.transforms import OrthographicProjection, Position3D, PanZoom, Viewport

# vertex = """
# uniform float translate;
# varying vec4  v_color;
# void main()
# {
#     fetch_uniforms();
#     v_color = color;
#     gl_Position = vec4(position.x+translate,position.y,0,1);
# }
# """

window = app.Window(1200,500, color=(1,1,1,1))

@window.event
def on_draw(dt):
    window.clear()
    quads.draw()
    labels.draw()


def add(names, values, xmin, xmax, ymin, ymax):
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
        y = y+dy/2
        labels.append(names[i].upper(), regular, color=c,
                      origin = (x,y,0), scale = 0.002, direction = (1,0,0),
                      anchor_x = "left", anchor_y = "center")

        x = xmax - 0.05*(xmax-xmin)
        labels.append(values[i].upper(), regular, color=c,
                      origin = (x,y,0), scale = 0.002, direction = (1,0,0),
                      anchor_x = "right", anchor_y = "center")

transform = PanZoom(OrthographicProjection(Position3D(), normalize=True)) + Viewport()
window.attach(transform)

quads  = collections.TriangleCollection(transform = transform)
labels = collections.GlyphCollection(transform = transform)
regular = FontManager().get_file("../glumpy/data/fonts/OpenSans-Regular.ttf")


xmin,xmax = -1.25, 1.25

names  = color.get("material:red").keys()[:-1][::-1]
values = color.get("material:red:*")[:-4][::-1]
add(names, values, xmin, xmax, -1.000, +1.000)

names  = ["A"+ v for v in color.get("material:red:accent").keys()[::-1]]
values = color.get("material:red:accent:*")[::-1]
add(names, values, xmin, xmax, -1.850, -1.050)


#add(base[5],      xmin, xmax, +1.050, +1.850)



time = 0
xstart, xstop, xcurr = 0,0,0

app.run()
