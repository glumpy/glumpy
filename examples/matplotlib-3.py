#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy.api.matplotlib import *

# Create a new figure
figure = Figure((12,12))


# Create a subplot on right, using panzoom interface (2d)
plot = figure.add_axes( [0.01, 0.01, 0.98, 0.98],
                        xscale = LinearScale(domain=[0.0,1.0], range=[0.0,1.0]),
                        yscale = LinearScale(domain=[0.0,1.0], range=[0,16*2*np.pi]),
                        projection = PolarProjection(),
                        interface = Trackball(name="trackball"),
                        facecolor=(0,0,1,0.25), aspect=None )

# Create a new collection of points
collection = PathCollection("agg+")

# Add a view of the collection on the subplot
plot.add_drawable(collection)

# Add some points

n = 2000
P = np.zeros((n,3))
P[:,0] = np.linspace(0,1,n)
P[:,1] = np.linspace(0,1,n)
P[:,2] = np.linspace(-1,1,n)
collection.append(P)
collection["linewidth"] = 3

# Show figure
figure.show()
