# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
from glumpy import app, __version__

console = app.Console(rows=32,cols=80)
window = app.Window(width = console.cols*console.cwidth*console.scale,
                    height = console.rows*console.cheight*console.scale,
                    color = (1,1,1,1))

@window.event
def on_draw(dt):
    window.clear(), console.draw()

@window.timer(1/30.0)
def timer(fps):
    console.clear()
    console.write("-------------------------------------------------------")
    console.write(" Glumpy version %s" % (__version__))
    console.write(" Window size: %dx%d" % (window.width, window.height))
    console.write(" Console size: %dx%d" % (console._rows, console._cols))
    console.write(" Backend: %s (%s)" % (window._backend.__name__,
                                        window._backend.__version__))
    console.write(" Actual FPS: %.2f frames/second" % (window.fps))
    console.write("-------------------------------------------------------")
    for line in repr(window.config).split("\n"):
        console.write(" "+line)
    console.write("-------------------------------------------------------")

window.attach(console)
app.run()
