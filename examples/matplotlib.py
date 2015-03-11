#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import gl, library
from glumpy.api import matplotlib
from glumpy.transforms import *
from glumpy.graphics.collections import *

# Create a new figure
figure = matplotlib.Figure((24,12))

# Create a subplot on left, using trackball interface (3d)
left  = figure.add_axes( [0.010, 0.01, 0.485, 0.98], interface = Trackball(),
                         facecolor=(1,0,0,0.25), aspect=1 )

# Create a subplot on right, using panzoom interface (2d)
right = figure.add_axes( [0.505, 0.01, 0.485, 0.98], interface = PanZoom(),
                         facecolor=(0,0,1,0.25), aspect=1 )

# Create a new point collection
collection = PointCollection("agg")

# Add a view of the collection on the left subplot
left.add(collection)

# Add a view of the collection on the right subplot
right.add(collection)

# Change xscale range on left subplot
left.transform['xscale']['range'] = -0.5,0.5

# Add some points
collection.append(np.random.normal(0,.5,(10000,3)))

# Show figure
figure.show()
