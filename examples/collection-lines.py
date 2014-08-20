#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import numpy as np
from  glumpy import app
from glumpy.graphics.collection import LineCollection


rows,cols = 16,20
n, p = rows*cols, 1000

lines = LineCollection()
lines.append(np.random.uniform(-1,1,(rows*cols*p,3)), itemsize=p)

for row in range(rows):
    for col in range(cols):
        i = row*cols+col
        lines[i]["position"][:,0] = np.linspace(-.95,+.95,p)
        lines[i]["position"][:,0] *= 1.0/float(cols)
        lines[i]["position"][:,0] += (2*col+1)/float(cols)-1
        lines[i]["position"][:,1] *= 0.5/float(rows)
        lines[i]["position"][:,1] += (2*row+1)/float(rows)-1
        r,g,b = np.random.uniform(.25,.75,3)
        lines[i]["color"] = r,g,b,1

window = app.Window(800,600)
@window.event
def on_draw(dt):
    window.clear(), lines.draw()

app.run()
