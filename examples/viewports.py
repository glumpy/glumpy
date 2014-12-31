#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gl, gloo
from glumpy.graphics.collections import PointCollection
from glumpy.transforms import Position3D, Trackball, OrthographicProjection, PanZoom

vertex = """ attribute vec2 position;
             void main() { gl_Position = vec4(position,0,1); } """

fragment = """ uniform vec4 color;
               void main() { gl_FragColor = color; } """

window = app.Window(width=800, height=800, color=(1,1,1,1))
program = gloo.Program(vertex, fragment, count=4)
program['position'] = [(-1,-1), (-1,+1), (+1,-1), (+1,+1)]

trackball = Trackball(Position3D(), aspect=1.0)
window.attach(trackball)
collection = PointCollection("agg", transform=trackball)
collection.append(np.random.normal(0,.5,(1000,3)), size=2)

vp0 = app.Viewport()
window.attach(vp0)
vp1 = app.Viewport(size=(.75,.75),position=(0.0,0.0), anchor=(0.0,0.0), aspect=1)
vp0.add(vp1)
vp2 = app.Viewport(size=(.75,.75),position=(0.5,0.5), anchor=(0.5,0.5), aspect=1)
vp1.add(vp2)
vp3 = app.Viewport(size=(.75,.75),position=(1.0,1.0), anchor=(1.0,1.0), aspect=1)
vp2.add(vp3)

@vp0.event
def on_draw(dt):
    window.clear()
    program["color"] = 0.75, 0.75, 0.75, 1.0
    program.draw(gl.GL_TRIANGLE_STRIP)
    collection["transform"].aspect = None
    collection.draw()
    collection["transform"].aspect = 1

@vp1.event
def on_draw(dt):
    program["color"] = 0.0, 1.0, 0.0, 1.0
    program.draw(gl.GL_TRIANGLE_STRIP)
    collection.draw()

@vp2.event
def on_draw(dt):
    program["color"] = 0.0, 0.0, 1.0, 1.0
    program.draw(gl.GL_TRIANGLE_STRIP)
    collection.draw()

@vp3.event
def on_draw(dt):
    program["color"] = 1.0, 0.0, 0.0, 1.0
    program.draw(gl.GL_TRIANGLE_STRIP)
    collection.draw()

@vp0.event
def on_mouse_press(x,y,button):
    print "VP0: mouse press at (%d,%d)" % (x,y)

@vp1.event
def on_mouse_press(x,y,button):
    print "VP1: mouse press at (%d,%d)" % (x,y)

@vp2.event
def on_mouse_press(x,y,button):
    print "VP2: mouse press at (%d,%d)" % (x,y)

@vp3.event
def on_mouse_press(x,y,button):
    print "VP3: mouse press at (%d,%d)" % (x,y)

app.run()
