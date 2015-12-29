# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import triangle
import numpy as np
from glumpy import app, gl
from glumpy.graphics.collections import TriangleCollection, PathCollection
from glumpy.transforms import Position, OrthographicProjection, PanZoom


def star(inner=0.5, outer=1.0, n=5):
    R = np.array( [inner,outer]*n)
    T = np.linspace(0,2*np.pi,2*n,endpoint=False)
    P = np.zeros((2*n,3))
    P[:,0]= R*np.cos(T)
    P[:,1]= R*np.sin(T)
    return P

window = app.Window(800, 800, color=(1,1,1,1))

def triangulate(P):
    n = len(P)
    S = np.repeat(np.arange(n+1),2)[1:-1]
    S[-2:] = n-1,0
    T = triangle.triangulate({'vertices': P[:,:2], 'segments': S}, "p")
    return  T["triangles"].ravel()

@window.event
def on_draw(dt):
    window.clear()
    triangles.draw()
    paths.draw()

@window.event
def on_init():
    gl.glEnable(gl.GL_DEPTH_TEST)

@window.event
def on_key_press(key, modifiers):
    if key == app.window.key.SPACE:
        transform.reset()


transform = PanZoom(OrthographicProjection(Position()))
triangles = TriangleCollection("agg", transform=transform, color='shared')
paths = PathCollection("agg", transform=transform, color='shared')
paths["linewidth"] = 10

P = star()
I = triangulate(P)

n = 64
for i in range(n):
    c = i/float(n)
    d = i
    x,y = np.random.uniform(0,800,2)
    s = 25
    triangles.append(P*s+(x,y,d), I, color=(0,0,0,.5))
    paths.append(P*s+(x,y,(d-1)), closed=True, color=(0,0,0,1))

window.attach(paths["transform"])
window.attach(paths["viewport"])
app.run()
