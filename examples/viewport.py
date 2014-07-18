#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import glumpy
import glumpy.gl as gl
import glumpy.app as app


window = app.Window(1024,1024)

left = app.Viewport(size=(.5,1), position=(0,0))
window.add(left)

right = app.Viewport(size=(.5,1.0), position=(.5,0))
window.add(right)

down = app.Viewport(size=(1.0,0.5), position=(0,0))
left.add(down)


@window.event
def on_draw():
    gl.glClearColor(1,1,1,1)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

@left.event
def on_draw():
    left.lock()
    if left.active: gl.glClearColor(0.75, 0.75, 0.75, 1.0)
    else:           gl.glClearColor(1.0, 0.0, 0.0, 1.0)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    left.unlock()

@right.event
def on_draw():
    right.lock()
    if right.active: gl.glClearColor(0.75, 0.75, 0.75, 1.0)
    else:            gl.glClearColor(0.0, 0.0, 1.0, 1.0)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    right.unlock()

@down.event
def on_draw():
    down.lock()
    if down.active: gl.glClearColor(0.75, 0.75, 0.75, 1.0)
    else:           gl.glClearColor(0.0, 1.0, 0.0, 1.0)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    down.unlock()


# @window.event
# def on_mouse_press(x, y, button):
#     print "Mouse press event on window"

# @left.event
# def on_mouse_press(x, y, button):
#     print "Mouse press event on left viewport"

# @right.event
# def on_mouse_press(x, y, button):
#     print "Mouse press event on right viewport"

# @down.event
# def on_mouse_press(x, y, button):
#     print "Mouse press event on down viewport"

# @window.event
# def on_mouse_release(x, y, button):
#     print "Mouse release event on window"

# @left.event
# def on_mouse_release(x, y, button):
#     print "Mouse release event on left viewport"

# @right.event
# def on_mouse_release(x, y, button):
#     print "Mouse release event on right viewport"

# @down.event
# def on_mouse_release(x, y, button):
#     print "Mouse release event on down viewport"

# @left.event
# def on_mouse_drag(x, y, dx, dy, button):
#     print "Mouse drag event on left viewport"

# @right.event
# def on_mouse_drag(x, y, dx, dy, button):
#     print "Mouse drag event on right viewport"

# @down.event
# def on_mouse_drag(x, y, dx, dy, button):
#     print "Mouse drag event on down viewport"

# @window.event
# def on_mouse_motion(x, y, dx, dy):
#     print "Mouse motion event on window"

# @left.event
# def on_mouse_motion(x, y, dx, dy):
#     print "Mouse motion event on left viewport"

# @right.event
# def on_mouse_motion(x, y, dx, dy):
#     print "Mouse motion event on right viewport"

# @down.event
# def on_mouse_motion(x, y, dx, dy):
#     print "Mouse motion event on down viewport"


app.run()
