# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy.api.matplotlib import *

# Create a new figure
figure = Figure((24,12))

# Create a subplot on left, using trackball interface (3d)
left = figure.add_axes( [0.010, 0.01, 0.485, 0.98],
                        xscale = LinearScale(clamp=True),
                        yscale = LinearScale(clamp=True),
                        zscale = LinearScale(clamp=True),
                        interface = Trackball(name="trackball"),
                        facecolor=(1,0,0,0.25), aspect=1 )

# Create a subplot on right, using panzoom interface (2d)
right = figure.add_axes( [0.505, 0.01, 0.485, 0.98],
                         xscale = LinearScale(domain=[-2.0,+2.0], range=[0.25,1.00]),
                         yscale = LinearScale(domain=[-2.0,+2.0], range=[0,2*np.pi]),
                         projection = PolarProjection(),
                         interface = Trackball(name="trackball"),
                         facecolor=(0,0,1,0.25), aspect=1 )

# Create a new collection of points
collection = PointCollection("agg")

# Add a view of the collection on the left subplot
left.add_drawable(collection)

# Add a view of the collection on the right subplot
right.add_drawable(collection)

# Add some points
collection.append(np.random.uniform(-2,2,(10000,3)))

# Show figure
figure.show()
