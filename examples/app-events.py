# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
from glumpy import app

window = app.Window()

@window.event
def on_init():
    print('Initialization')

@window.event
def on_draw(dt):
    # print 'Draw after %.1f milliseconds' % (1000*dt)
    window.clear()

@window.event
def on_resize(width,height):
    print('Window resized (width=%.1f, height=%.1f)'% (width,height))

@window.timer(1.0) # frames per second
def timer(elapsed):
    print('Timed event (%.2f second(s) elapsed)' % elapsed)

# @window.event
# def on_idle(dt):
#     print 'Idle event'

@window.event
def on_key_press(symbol, modifiers):
    print('Key pressed (symbol=%s, modifiers=%s)'% (symbol,modifiers))

@window.event
def on_character(character):
    print('Character entered (chracter: %s)'% character)

@window.event
def on_key_release(symbol, modifiers):
    print('Key released (symbol=%s, modifiers=%s)'% (symbol,modifiers))

@window.event
def on_mouse_press(x, y, button):
    print('Mouse button pressed (x=%.1f, y=%.1f, button=%d)' % (x,y,button))

@window.event
def on_mouse_release(x, y, button):
    print('Mouse button released (x=%.1f, y=%.1f, button=%d)' % (x,y,button))

@window.event
def on_mouse_motion(x, y, dx, dy):
    print('Mouse motion (x=%.1f, y=%.1f, dx=%.1f, dy=%.1f)' % (x,y,dx,dy))

@window.event
def on_mouse_drag(x, y, dx, dy, button):
    print('Mouse drag (x=%.1f, y=%.1f, dx=%.1f, dy=%.1f, button=%d)' % (x,y,dx,dy,button))

@window.event
def on_mouse_scroll(x, y, dx, dy):
    print('Mouse scroll (x=%.1f, y=%.1f, dx=%.1f, dy=%.1f)' % (x,y,dx,dy))

app.run(framerate=10)
