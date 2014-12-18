#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import numpy as np
from  glumpy import app
from glumpy.graphics.collection import MarkerCollection

n = 1000
C = MarkerCollection(orientation='local')

C.append(np.random.uniform(-1,1,(n,3)),
         bg_color = np.random.uniform(0,1,(n,4)),
         size = 64, fg_color=(0,0,0,1))

window = app.Window(1024,1024, color=(1,1,1,1))

@window.event
def on_draw(dt):
    window.clear()
    C.draw()
    C['orientation'] += np.random.uniform(0.0,0.1,len(C))
    del C[0]
    if not len(C):
        app.quit()

app.run()
