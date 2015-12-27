# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import sys
import numpy as np
from scipy.spatial.distance import cdist

from glumpy import app, collections
from glumpy.transforms import Position, OrthographicProjection, Viewport

window = app.Window(width=800, height=800, color=(1,1,1,1))

@window.event
def on_draw(dt):
    window.clear()
    segments.draw()
    markers.draw()

@window.event
def on_mouse_press(x, y, button):
    global N, selected

    D = N - [x, window.height-y, 0]
    D = np.sqrt((D**2).sum(axis=1))
    selected = np.argmin(D)
    if D[selected] > 10:
        selected = -1

@window.event
def on_mouse_release(x, y, button):
    global selected
    selected = -1

@window.event
def on_mouse_drag(x, y, dx, dy, button):
    global N, selected
    if selected > -1 :
        N[selected] = x,window.height-y,0

@window.timer(1.0/60.0)
def on_timer(dt):
    global N, A, S, src, tgt

    X,Y, XY = N[:,0], N[:,1], N[:,:2]
    XY_ = XY.copy()

    # To be adpated depending on the topology of the graph
    attraction = 0.4
    repulsion = 25
    length = 30

    # Global nodes centering
    # ----------------------
    x,y = window.width/2, window.height/2
    XY += 0.01*([x,y] - XY)

    # Linked nodes attraction
    # -----------------------
    D = N[src]- N[tgt]
    L = np.maximum(np.sqrt((D*D).sum(axis=1)),1)
    L = (L - length)/L
    D *= attraction*L[:,np.newaxis]
    X -= .5*np.bincount(src, D[:,0], minlength=len(N))
    Y -= .5*np.bincount(src, D[:,1], minlength=len(N))
    X += .5*np.bincount(tgt, D[:,0], minlength=len(N))
    Y += .5*np.bincount(tgt, D[:,1], minlength=len(N))

    # Global nodes repulsion
    # ----------------------
    dist = np.maximum(cdist(XY,XY,'sqeuclidean'),1)
    D = np.empty((len(N),len(N),2))
    D[...,0] = np.subtract.outer(X,X)/dist
    D[...,1] = np.subtract.outer(Y,Y)/dist
    R = D.sum(axis=1)
    XY += repulsion*R/np.sqrt(((R*R).sum(axis=0)))

    # Cancel move for selected node
    # -----------------------------
    if selected > -1:
        XY[selected] = XY_[selected]

    # Update markers and segments
    # ---------------------------
    markers["position"] = N
    segments["P0"] = np.repeat(N[src],4,axis=0)
    segments["P1"] = np.repeat(N[tgt],4,axis=0)


# Simple graph
# n = 11
# N = np.random.uniform(150, 650, (n,3)) * (1,1,0)
# A = np.zeros((n,n))
# A[[0,1,2,3,0,1,3,4,5,6,7,8, 9,10, 8,7],
#   [1,2,3,0,2,3,4,5,6,7,8,9,10, 7,10,9] ] = 1

# # Random graph
# n = 250
# N = np.random.uniform(0, 800, (n,3)) * (1,1,0)
# A = (cdist(N[:,:2],N[:,:2]) < 75)
# N = np.random.uniform(390, 410, (n,3)) * (1,1,0)

# Balanced graph
depth,branch = 4, 3
# sum of geometric series r!=1
n = int((1-branch**(depth+1))/(1-branch)) if branch > 1 else 2
N = np.random.uniform(0, 800, (n,3)) * (1,1,0)
A = np.zeros((n,n), dtype=bool)
nodes=iter(range(n))
parents=[next(nodes)]
while parents:
    source=parents.pop(0)
    for i in range(branch):
        try:
            target=next(nodes)
            parents.append(target)
            A[source,target] = 1
        except StopIteration:
            break

# Current selected node
selected = -1

# Get edges
src,tgt = np.nonzero(A)

transform = OrthographicProjection(Position(), aspect=None)
viewport = Viewport()


markers = collections.MarkerCollection(marker='disc', transform=transform, viewport=viewport)
markers.append(N, size=15, linewidth=2, itemsize=1,
               fg_color=(1,1,1,1), bg_color=(1,.5,.5,1))
segments = collections.SegmentCollection('agg', transform=transform, viewport=viewport)
segments.append(N[src], N[tgt], linewidth=1.0, itemsize=1,
                color=(0.75,0.75,0.75,1.00))

window.attach(transform)
window.attach(viewport)

app.run()
