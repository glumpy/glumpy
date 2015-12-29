# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import math
from glumpy import app, gloo, gl

vertex = """
  uniform float scale;
  attribute vec2 position;
  attribute vec4 color;
  varying vec4 v_color;
  void main()
  {
    gl_Position = vec4(scale*position, 0.0, 1.0);
    v_color = color;
  } """

fragment = """
  varying vec4 v_color;
  void main()
  {
      gl_FragColor = v_color;
  } """

# Build the program and corresponding buffers (with 4 vertices)
quad = gloo.Program(vertex, fragment, count=4)

# Upload data into GPU
quad['color'] = [ (1,0,0,1), (0,1,0,1), (0,0,1,1), (1,1,0,1) ]
quad['position'] = [ (-1,-1),   (-1,+1),   (+1,-1),   (+1,+1)   ]
quad['scale'] = 1.0

# Create a window with a valid GL context
window = app.Window()

time = 0.0

# Tell glumpy what needs to be done at each redraw
@window.event
def on_draw(dt):
    global time
    time += dt
    window.clear()
    quad["scale"] = math.cos(time)
    quad.draw(gl.GL_TRIANGLE_STRIP)

# Run the app
app.run()
