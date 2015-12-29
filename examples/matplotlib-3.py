# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy.api.matplotlib import *

# Create a new figure
figure = Figure((12,12))


# Create a subplot on right, using panzoom interface (2d)
plot = figure.add_axes( [0.01, 0.01, 0.98, 0.98],
                        xscale = LinearScale(domain=[0.0,1.0], range=[0.0,1.0]),
                        yscale = LinearScale(domain=[0.0,1.0], range=[0,2*np.pi]),
                        projection = PolarProjection(),
                        interface = Trackball(name="trackball"),
                        facecolor=(0,0,1,0.25), aspect=None )

# Create a new collection of points
collection = PathCollection("agg+")

# Add a view of the collection on the subplot
plot.add_drawable(collection)

# Add some points
n = 1000
P = np.zeros((n,3))
P[:,0] = np.linspace(1, 0,n)
P[:,1] = np.linspace(0,5,n)
P[:,2] = np.linspace(-1,1,n)
collection.append(P)
collection["linewidth"] = 1

# Frame
n = 100
xmin,xmax = +0.0, 1.0
ymin,ymax = +0.0, 1.0
zmin,zmax = -1.0, 1.0
frame = PathCollection("agg+")
plot.add_drawable(frame)
frame["linewidth"] = 2.5

P = np.zeros((n,3))

P[:,0] = xmax
P[:,1] = np.linspace(ymin,ymax,n)
P[:,2] = zmin
frame.append(P)

P[:,0] = np.linspace(xmin,xmax,n)
P[:,1] = ymin
P[:,2] = zmin
frame.append(P)

P[:,0] = xmin
P[:,1] = ymin
P[:,2] = np.linspace(zmin,zmax,n)
frame.append(P)

# Ticks
ticks = SegmentCollection("agg", linewidth="local")
plot.add_drawable(ticks)

n = 23
P0 = np.zeros((n-2,3))
P1 = np.zeros((n-2,3))
P0[:,0] = np.linspace(xmin,xmax,n)[1:-1]
P0[:,1] = ymin - 0.0
P0[:,2] = zmin
P1[:,0] = np.linspace(xmin,xmax,n)[1:-1]
P1[:,1] = ymin + 0.015 * (ymax-ymin)
P1[:,2] = zmin
ticks.append(P0, P1, linewidth=2.5)

P0 = np.zeros((n-1,3))
P1 = np.zeros((n-1,3))
P0[:,0] = xmax + 0.015
P0[:,1] = np.linspace(ymin,ymax,n)[1:]
P0[:,2] = zmin
P1[:,0] = xmax - 0.025 * (xmax-xmin)
P1[:,1] = np.linspace(ymin,ymax,n)[1:]
P1[:,2] = zmin
ticks.append(P0, P1, linewidth=2.5)

P0 = np.zeros((n-1,3))
P1 = np.zeros((n-1,3))
P0[:,0] = xmin + 0.025
P0[:,1] = 0
P0[:,2] = np.linspace(zmin,zmax,n)[1:]
P1[:,0] = xmin - 0.015 * (xmax-xmin)
P1[:,1] = 0
P1[:,2] = np.linspace(zmin,zmax,n)[1:]
ticks.append(P0, P1, linewidth=2.5)


# Show figure
figure.show()
