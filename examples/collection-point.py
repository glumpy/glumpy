#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app
from glumpy.graphics.collection import PointCollection

window = app.Window(1024,1024, color=(1,1,1,1))

n = 10000
C = PointCollection("agg", color="shared")
C.append(np.random.normal(0,.25,(n,3)), itemsize=n/2)
C["color"] = (1,0,0,1), (0,0,1,1)


@window.event
def on_draw(dt):
    window.clear()
    C.draw()

app.run()
