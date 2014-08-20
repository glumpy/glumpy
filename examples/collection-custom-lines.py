#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import numpy as np
from  glumpy import app
from glumpy.graphics.collection import LineCollection


vertex = """
// Those are added automatically by the collection
// -----------------------------------------------
// uniform   sampler2D uniforms;
// uniform   vec3      uniforms_shape;
// attribute float     collection_index;
//
// attribute vec3 position;
// attribute vec4 color;
// ... user-defined through collection init dtypes
// -----------------------------------------------

uniform float rows, cols;
varying float v_x;
varying vec4 v_color;
void main()
{
    // This line is mandatory and is responsible for fetching uniforms
    // from the underlying uniform texture
    fetch_uniforms();

    // color can end up being an attribute or a varying
    // If you want to make sure to pass it to the fragment,
    // It's better to define it here explicitly
    if (selected > 0.0)
        v_color = vec4(1,1,1,1);
    else
        v_color = color;

    float index = collection_index;

    // Compute row/col from collection_index
    float col = mod(index,cols) + 0.5;
    float row = floor(index/cols) + 0.5;
    float x = -1.0 + col * (2.0/cols);
    float y = -1.0 + row * (2.0/rows);
    float width = 0.95 / (1.0*cols);
    float height = 0.95 / (1.0*rows) * amplitude;

    v_x = xscale*position.x;
    gl_Position = vec4(x + width*xscale*position.x, y + height*position.y, 0.0, 1.0);
}
"""

fragment = """
// Collection varyings are not propagated to the fragment shader
// -------------------------------------------------------------
varying float v_x;
varying vec4 v_color;
void main(void)
{
    if( v_x < -0.95) discard;
    if( v_x > +0.95) discard;
    gl_FragColor = v_color;
}
"""


rows,cols = 16,20
n, p = rows*cols, 1000
lines = LineCollection(dtypes = [("amplitude", np.float32, 1),
                                 ("selected",  np.float32, 1),
                                 ("xscale",    np.float32, 1)],
                       scopes = {"amplitude" : "shared",
                                 "selected" : "shared",
                                 "xscale" : "shared"},
                       vertex=vertex, fragment=fragment )
lines["rows"] = rows
lines["cols"] = cols
lines.append(np.random.uniform(-1,1,(n*p,3)), itemsize=p)
lines["position"][:,0] = np.tile(np.linspace(-1,+1,p),n)
lines["amplitude"][:n] = np.random.uniform(0.25,0.75,n)
lines["color"][:n] = np.random.uniform(0.25,0.75,(n,4))
lines["selected"] = 0.0
lines["xscale"][:n] = np.random.uniform(1,25,n)

window = app.Window(800,600)
@window.event
def on_draw(dt):
    window.clear(), lines.draw()
    Y = lines["position"][:,1].reshape(n,p)
    Y[:,:-10] = Y[:,10:]
    Y[:,-10:] = np.random.uniform(-1,1, (n,10))

def get_index(x,y):
    """ Find the index of the plot under mouse """
    y = window.height-y
    col = int(x/float(window.width)*cols) % cols
    row = int(y/float(window.height)*rows) % rows
    return row*cols + col

@window.event
def on_mouse_motion(x,y,dx,dy):
    index = get_index(x,y)
    lines["selected"] = 0
    lines["selected"][index] = 1

@window.event
def on_mouse_scroll(x, y, dx, dy):
    index = get_index(x,y)
    dx = np.sign(dy) * .05
    lines["xscale"][index] *= np.exp(2.5*dx)
    lines["xscale"][index] = min(max(1.0, lines["xscale"][index]),100)

app.run()
