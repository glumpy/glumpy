==========
Quickstart
==========

Hello World!
============

We'll begin with the requisite "Hello, World" introduction. This program will
open a window with some text in it and wait to be closed. You can find the
entire program in the `hello_world.py file <github.com>`_.

Begin by importing the glumpy package:

.. code:: python

   import glumpy

Create a Window by calling its default constructor. The window will be visible
as soon as it's created, and will have reasonable default values for all its
parameters:


.. code:: python

   window = glumpy.Window(width=512, height=512)

To display the text, we'll create a Label. Keyword arguments are used to set
the font, position and anchorage of the label:


.. code:: python

   font  = glumpy.text.Font("Vera.ttf", 64)
   label = glumpy.text.Label(u"Hello World !", font,
                             anchor_x = 'center', anchor_y = 'center')

An on_draw event is dispatched to the window to give it a chance to redraw its
contents. glumpy provides several ways to attach event handlers to objects; a
simple way is to use a decorator:

.. code:: python

   @window.event
   def on_draw():
       window.clear()
       label.draw(x=256, y=256, color=(1,1,1,1))

Within the on_draw handler the window is cleared to the default background
color (black), and the label is drawn.

Finally, call:

.. code:: python

   glumpy.run()

To let glumpy respond to application events such as the mouse and
keyboard. Your event handlers will now be called as required, and the *run*
method will return only when all application windows have been closed.


Hello Lena!
===========

In this example we'll load an image from the examples data directory and
display it within the window while enforcing the image aspect such that
proportion of the image are conserved when user resize the window.
You can find the entire program in the `image.py file <github.com>`_.


.. code-block:: python

   import glumpy

   img = glumpy.graphics.Image("data/lena.png",
                               anchor_x = 'center', anchor_y = 'center')
   aspect = float(img.width)/float(img.height)
   window = glumpy.Window(aspect = aspect)

   @window.event
   def on_draw():
      window.clear()
      with window.viewport():
          img.draw(x=0, y=0)

   app.run()


Hello GLSL!
===========

The previous example made implicit use of shaders to display things on
screen. However, the real power of modern OpenGL lies in the possibility of
writing custom shaders to draw virutally anything. We'll now see how to write a
shader from scratch. Let's start by creating a window as usual.

.. code:: python

   import glumpy.gl as gl
   import glumpy.app as app
   import glumpy.gloo as gloo

   window = Window()

What has not be explained previously is that the position on the window surface
can be accessed in many different ways, until now, we have been using an
implicit normalized representation of the surface that goes from [-1,-1] to
[+1,+1]. This means that if we want to draw something, we need to have our
coordinates transformed such that they fit within this range. Suppose we want
to display a simple quad that cover the whole window:

.. code:: python

   quad = [(-1, -1), (-1, +1), (+1, -1), (+1, +1)]

We need to tell OpenGL how to display this object and we thus need a program
that is composed of a **vertex shader** and a **fragment shader**. Let's write first
the vertex shader that tell OpenGL how to transform vertex coordinates into a
normalized coordinates (easy since our quad is already normalized).

.. code::

   vec2 attribute position;
   void main()
   {
       gl_Position = vec4(position, 0.0, 1.0);
   }

The first line declares that a vertex is made of one attribute that is a vector
of two floats and named ``position`` such that it can be used in the main
function. ``gl_Position`` is a special keyword of GLSL that tell the vertex
shader the final position of the vertex. It is a four-dimensions vector because
OpenGL uses quaternion. We can now consider the fragment shader in order to
tell OpenGL the color to draw each fragment that will be contained within our
object.

.. note:: At this point, we still don't known what our shape will be, we only
          have some vertices placed on screen.

.. code::

   void main()
   {
       gl_FragColor = vec4(1.0, 1.0, 1.0, 1.0);
   }

``gl_FragColor`` is another special GLSL keyword that contains the final
fragment (=pixel) color and uses an RGBA normalized encoding. In the program
above, any fragment will be white. We're almost done and we need now to create
a program:

.. code:: python

   program = gloo.Program(vertex, fragment, 4)

and we need to fill the attributes. The most simple and straightforward way to
do that is:

.. code:: python

   program['position'] = quad
