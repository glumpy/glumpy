# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
#
# modified examples/tutorial/quad-simple.py
from glumpy import app, gloo, gl
import numpy as np

vertex = """
  uniform float scale;
  in vec2 position;
  in vec4 color;
  out vec4 v_color;
  void main()
  {
    gl_Position = vec4(scale*position, 0.0, 1.0);
    v_color = color;
  } """

fragment = """
  in vec4 v_color;
  out vec4 FragColor;
  void main()
  {
      FragColor = v_color;
  } """

app.use('glfw', api='GL', major=3, minor=3, profile='core')

# Create a window with a valid GL context
window = app.Window()

# Build the program and corresponding buffers (with 4 vertices)
quad = gloo.Program(vertex, fragment, count=4, version="330")
dtype = [('color', np.float32, 4),
         ('position', np.float32, 2)]
quad_arrays_0 = np.zeros(4, dtype).view(gloo.VertexArray)
# Four colors
quad_arrays_0['color'] = [ (1,0,0,1), (0,1,0,1), (0,0,1,1), (1,1,0,1) ]
quad_arrays_0['position'] = [ (-1,-1),   (-1,+1),   (+1,-1),   (+1,+1)   ]

quad_arrays_1 = np.zeros(4, dtype).view(gloo.VertexArray)
# All red data
quad_arrays_1['color'] = [ (1,0,0,1), (1,0,0,1), (1,0,0,1), (1,0,0,1) ]
quad_arrays_1['position'] = [ (-1,-1),   (-1,+1),   (+1,-1),   (+1,+1)   ]

quad['scale'] = 1.0


# Tell glumpy what needs to be done at each redraw
count = 0
@window.event
def on_draw(dt):
    global count
    window.clear()
    if count % 2 == 0:
        quad.bind(quad_arrays_0)
        quad.draw(gl.GL_TRIANGLE_STRIP)
    else:
        quad.bind(quad_arrays_1)
        quad.draw(gl.GL_TRIANGLE_STRIP)
    count += 1

# Run the app
app.run(framerate=1)
