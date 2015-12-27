# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gl, gloo
from glumpy.transforms import Position, OrthographicProjection, PanZoom

# Create window
window = app.Window(width=2*512, height=512, color=(1,1,1,1))

# What to draw when necessary
@window.event
def on_draw(dt):
    window.clear()
    program.draw(gl.GL_POINTS)
    program['orientation'][-1] += np.pi/1024.0

# Setup some markers
n = 500+1
data = np.zeros(n, dtype=[('position',    np.float32, 2),
                          ('fg_color',    np.float32, 4),
                          ('bg_color',    np.float32, 4),
                          ('size',        np.float32, 1),
                          ('orientation', np.float32, 1),
                          ('linewidth',   np.float32, 1)])
data = data.view(gloo.VertexBuffer)
data['linewidth'] = 1
data['fg_color'] = 0, 0, 0, 1
data['bg_color'] = 1, 1, 1, 0
data['orientation'] = 0
radius, theta, dtheta = 250.0, 0.0, 5.5 / 180.0 * np.pi
for i in range(500):
    theta += dtheta
    x = 256 + radius * np.cos(theta)
    y = 256 + radius * np.sin(theta)
    r = 10.0 - i * 0.02
    radius -= 0.45
    data['orientation'][i] = theta - np.pi/2
    data['position'][i] = x, y
    data['size'][i] = 2 * r
    data['linewidth'][i] = 1

data['position'][-1]    = 512+256, 256
data['size'][-1]        = 512/np.sqrt(2)
data['linewidth'][-1]   = 3.0
data['fg_color'][-1]    = 0, 0, 0, 1
data['bg_color'][-1]    = .95, .95, .95, 1
data['orientation'][-1] = 0

program = gloo.Program("markers/marker.vert", "markers/marker.frag")
program.bind(data)
program['antialias'] = 1.00
program['marker']    = "square"
program['paint']     = "stroke"
transform = OrthographicProjection(Position("position"))
program['transform'] = transform
window.attach(transform)

app.run()
