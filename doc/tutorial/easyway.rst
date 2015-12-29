============
The easy way
============

As we've seen in the previous section, displaying a simple quad using modern GL
is quite tedious and requires a fair number of operations. The goal of glumpy
is to make this process both easy and intuitive. Let's consider again the
vertex and fragment code:

.. code:: python

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


The exact same example can now be rewritten as:

.. code:: python

   from glumpy import app, gloo, gl

   # Build the program and corresponding buffers (with 4 vertices)
   quad = gloo.Program(vertex, fragment, count=4)

   # Upload data into GPU
   quad['color'] = [ (1,0,0,1), (0,1,0,1), (0,0,1,1), (1,1,0,1) ]
   quad['position'] = [ (-1,-1),   (-1,+1),   (+1,-1),   (+1,+1)   ]
   quad['scale'] = 1.0

   # Create a window with a valid GL context
   window = app.Window()

   # Tell glumpy what needs to be done at each redraw
   @window.event
   def on_draw(dt):
       window.clear()
       quad.draw(gl.GL_TRIANGLE_STRIP)

   # Run the app
   app.run()


.. image:: ../_static/hello-world.png
   :target: scripts/hello-world-gl.py
   :align: right
   :width: 40%

Glumpy takes care of building the buffer because we specified the vertex count
value and will also bind the relevant attributes and uniforms to the program.
You should obtain the same output as in previous section.

`Full source code <https://github.com/glumpy/glumpy/blob/master/examples/tutorial/quad-simple.py>`_ is available on github


A step further
==============

The nice thing with gloo is that it takes care of any change in uniform or
attribute values. If you change them through the program interface, these
values will be updated on the GPU just-in-time. So, let's have some animation
by making the scale value to oscillate betwen 0 and 1. To do this, we need a
simple timer function where we'll update the scale value:

.. code:: python

   time = 0.0
          
   @window.event
   def on_draw(dt):
       global time

       time += dt
       window.clear()
       quad['scale'] = np.cos(time)
       quad.draw(gl.GL_TRIANGLE_STRIP)

       
Exercices
=========

**Quad rotation** Instead of scaling the quad, try to make it rotate. Note that
you have access to the sin and cos function from within the shader.
(`solution 1 <https://github.com/glumpy/glumpy/blob/master/examples/tutorial/quad-rotation.py>`_)

**Viewport aspect**: Since the viewport is normalized, this means the aspect
ratio of our quad is not always 1, it can become wider or taller, depending on
how the actual shape of the window. How to change the reshape function
(viewport call) to achieve a constant ratio of 1 (square) ?
(`solution 2 <https://github.com/glumpy/glumpy/blob/master/examples/tutorial/viewport-aspect.py>`_)

**Quad aspect**: In the previous exercice, we manipulated the viewport such a
to have a constant ratio of 1 for the viewport. We could however only
manipulate the vertex position from within the shader, provided we know the
size of the viewport, how would you do this ?
(`solution 3 <https://github.com/glumpy/glumpy/blob/master/examples/tutorial/quad-aspect.py>`_)
