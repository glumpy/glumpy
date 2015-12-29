# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, glm
from glumpy.graphics.text import FontManager
from glumpy.transforms import Position, Trackball, Viewport
from glumpy.graphics.collections import GlyphCollection
from glumpy.graphics.collections import PathCollection
from glumpy.graphics.collections import SegmentCollection


window = app.Window(width=1000, height=800, color=(1,1,1,1))

@window.event
def on_draw(dt):
    window.clear()
    ticks.draw()
    labels.draw()
    paths.draw()

@window.event
def on_key_press(key, modifiers):
    if key == app.window.key.SPACE:
        reset()

def reset():
    transform.theta = 0
    transform.phi = 0
    transform.zoom = 16.5


transform = Trackball(Position())
viewport = Viewport()
labels = GlyphCollection(transform=transform, viewport=viewport)
paths = PathCollection(mode="agg+", transform=transform, viewport=viewport)
ticks = SegmentCollection(mode="agg", transform=transform, viewport=viewport,
                          linewidth='local', color='local')



# xmin,xmax = 0,800
# ymin,ymax = 0,800
xmin,xmax = -1,1
ymin,ymax = -1,1


z = 0

regular = FontManager.get("OpenSans-Regular.ttf")
bold    = FontManager.get("OpenSans-Bold.ttf")
n = 11
scale = 0.001
for i,y in enumerate(np.linspace(xmin,xmax,n)):
    text = "%.2f" % (i/10.0)
    labels.append(text, regular,
                  origin = (1.05,y,z), scale = scale, direction = (1,0,0),
                  anchor_x = "left", anchor_y = "center")
    labels.append(text, regular, origin = (y, -1.05, z),
                  scale= scale, direction = (1,0,0),
                  anchor_x = "center", anchor_y = "top")

title = "Lorenz strange attractor"
labels.append(title, bold, origin = (0, 1.1, z),
              scale= 2*scale, direction = (1,0,0),
              anchor_x = "center", anchor_y = "center")





# Frame
# -------------------------------------
P0 = [(xmin,ymin,z), (xmin,ymax,z), (xmax,ymax,z), (xmax,ymin,z)]
P1 = [(xmin,ymax,z), (xmax,ymax,z), (xmax,ymin,z), (xmin,ymin,z)]
ticks.append(P0, P1, linewidth=2)

# Grids
# -------------------------------------
n = 11
P0 = np.zeros((n-2,3))
P1 = np.zeros((n-2,3))

P0[:,0] = np.linspace(xmin,xmax,n)[1:-1]
P0[:,1] = ymin
P0[:,2] = z
P1[:,0] = np.linspace(xmin,xmax,n)[1:-1]
P1[:,1] = ymax
P1[:,2] = z
ticks.append(P0, P1, linewidth=1, color=(0,0,0,.25))

P0 = np.zeros((n-2,3))
P1 = np.zeros((n-2,3))
P0[:,0] = xmin
P0[:,1] = np.linspace(ymin,ymax,n)[1:-1]
P0[:,2] = z
P1[:,0] = xmax
P1[:,1] = np.linspace(ymin,ymax,n)[1:-1]
P1[:,2] = z
ticks.append(P0, P1, linewidth=1, color=(0,0,0,.25))


# Majors
# -------------------------------------
n = 11
P0 = np.zeros((n-2,3))
P1 = np.zeros((n-2,3))
P0[:,0] = np.linspace(xmin,xmax,n)[1:-1]
P0[:,1] = ymin - 0.015
P0[:,2] = z
P1[:,0] = np.linspace(xmin,xmax,n)[1:-1]
P1[:,1] = ymin + 0.025 * (ymax-ymin)
P1[:,2] = z
ticks.append(P0, P1, linewidth=1.5)
P0[:,1] = ymax + 0.015
P1[:,1] = ymax - 0.025 * (ymax-ymin)
ticks.append(P0, P1, linewidth=1.5)

P0 = np.zeros((n-2,3))
P1 = np.zeros((n-2,3))
P0[:,0] = xmin - 0.015
P0[:,1] = np.linspace(ymin,ymax,n)[1:-1]
P0[:,2] = z
P1[:,0] = xmin + 0.025 * (xmax-xmin)
P1[:,1] = np.linspace(ymin,ymax,n)[1:-1]
P1[:,2] = z
ticks.append(P0, P1, linewidth=1.5)
P0[:,0] = xmax + 0.015
P1[:,0] = xmax - 0.025 * (xmax-xmin)
ticks.append(P0, P1, linewidth=1.5)


# Minors
# -------------------------------------
n = 111
P0 = np.zeros((n-2,3))
P1 = np.zeros((n-2,3))
P0[:,0] = np.linspace(xmin,xmax,n)[1:-1]
P0[:,1] = ymin
P0[:,2] = z
P1[:,0] = np.linspace(xmin,xmax,n)[1:-1]
P1[:,1] = ymin + 0.0125 * (ymax-ymin)
P1[:,2] = z
ticks.append(P0, P1, linewidth=1)
P0[:,1] = ymax
P1[:,1] = ymax - 0.0125 * (ymax-ymin)
ticks.append(P0, P1, linewidth=1)

P0 = np.zeros((n-2,3))
P1 = np.zeros((n-2,3))
P0[:,0] = xmin
P0[:,1] = np.linspace(ymin,ymax,n)[1:-1]
P0[:,2] = z
P1[:,0] = xmin + 0.0125 * (xmax-xmin)
P1[:,1] = np.linspace(ymin,ymax,n)[1:-1]
P1[:,2] = z
ticks.append(P0, P1, linewidth=1)
P0[:,0] = xmax
P1[:,0] = xmax - 0.0125 * (xmax-xmin)
ticks.append(P0, P1, linewidth=1)


def lorenz(n=50000):
    def iterate(P, s=10, r=28, b=2.667, dt=0.01):
        x, y, z = P
        x_dot = s*(y - x)
        y_dot = r*x - y - x*z
        z_dot = x*y - b*z
        return dt*x_dot, dt*y_dot, dt*z_dot

    # Need one more for the initial values
    P = np.empty((n+1,3))

    # Setting initial values
    P[0] = 0., 1., 1.05

    # Stepping through "time"
    dt = 100.0/n
    for i in range(n) :
        # Derivatives of the X, Y, Z state
        P[i+1] = P[i] + iterate(P[i], dt=dt)

    # Normalize
    vmin,vmax = P.min(),P.max()
    P = 2*(P-vmin)/(vmax-vmin) - 1

    # Centering
    P[:,0] -= (P[:,0].max() + P[:,0].min())/2.0
    P[:,1] -= (P[:,1].max() + P[:,1].min())/2.0
    P[:,2] -= (P[:,2].max() + P[:,2].min())/2.0

    return P


paths.append(lorenz(), color=(0,0,1,1), closed=False)
paths["color"] = 0,0,1,1
reset()


window.attach(paths["transform"])
window.attach(paths["viewport"])
app.run()
