# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
from glumpy import app, gloo, gl
from glumpy.transforms import PanZoom, Position

app.use("pyimgui")

vertex = """
    uniform float theta;
    attribute vec4 color;
    attribute vec2 position;
    varying vec4 v_color;
    void main()
    {
        float ct = cos(theta);
        float st = sin(theta);
        float x = 0.75* (position.x*ct - position.y*st);
        float y = 0.75* (position.x*st + position.y*ct);
        vec4 pos =  (vec4(x, y, 0.0, 1.0));
        gl_Position = <transform>;
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
quad['theta'] = 0

# Create a window with a valid GL context
window = app.Window(width=1024, height=768, color=(.1,.1,.4,1))

transform = PanZoom(Position("pos"),aspect=1)
quad['transform'] = transform
window.attach(transform)

theta = 0.0
speed = 1.0

# Tell glumpy what needs to be done at each redraw
@window.event
def on_gui(dt):
    gui = window.gui
    gui.begin("Custom window", True)
    gui.text("Bar")
    gui.text_colored("Eggs", 0.2, 1., 0.)
    gui.end()

# Tell glumpy what needs to be done at each redraw
@window.event
def on_draw(dt):
    window.clear()
    quad['theta'] += dt*speed
    quad.draw(gl.GL_TRIANGLE_STRIP)


# Run the app
app.run()

