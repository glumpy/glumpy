===============
Getting started
===============

Getting started with a new library or framework can be daunting, especially
when presented with a large amount of reference material to read.  This
chapter gives a very quick introduction to glumpy without covering any of the
details.

**Content**

.. contents::
    :local:


Creating a window
=================

Creating a new window is straightforward:

.. code:: python

   from glumpy import app
   window = app.Window()
   app.run()
   
You should see immediately a new window on your desktop with possibly some
garbage on it. The reason for the garbage is that we do not clear the window.
A better minimal version is thus:

.. code:: python

   from glumpy import app

   window = app.Window()

   @window.event
   def on_draw(dt):
       window.clear()
   
   app.run()

In this version, we use the :meth:`on_draw` event that is dispatched every time
a redraw is needed for the window.  Within our `on_draw` handler, the window is
cleared to the default background color (black).

The final call to the `app.run()` gives control to the glumpy application loop
that will respond to application events such as the mouse and the keyboard.

.. note::

   The **run** method only returns when all application windows have been
   closed unless the program has been launched in **interactive mode.** If you
   start the program using the ``--interactive`` switch, the `app.run()` is no
   longer blocking.
   

Displaying a quad
=================

Modern OpenGL is very powerful but hard to understand and program. Any drawing
operation requires a number of preparatory steps that make it cumbersome to use
without additonal libraries. Glumpy offers an easier access through the
:mod:`gloo` interface which is a kind of glue between numpy and OpenGL.

Let's see how to draw a full-window colored quad using glumpy. First steps is
to import the relevant modules and create the window.
     

.. code:: python

   from glumpy import app, gloo, gl

   window = app.Window()

We then need to create a GLSL program that will be in charge of displaying a
quad. To do this, we first have to write a vertex and a fragment shader that
will tell OpenGL exactly what and how to draw things. No need to understand
them yet but the important point here is that those program are just text
strings.


.. code:: C

   vertex = """
            attribute vec2 position;
            void main()
            {
                gl_Position = vec4(position, 0.0, 1.0);
            } """

   fragment = """
              uniform vec4 color;
              void main() {
                  gl_FragColor = color;
              } """

   quad = gloo.Program(vertex, fragment, count=4)

The nice thing with the :mod:`gloo` interface is that you can now directly
upload some data to the GPU using convenient notation. The `position` index
directly relates to the `position` attribute within the vertex shader and the
`color` index relates to the `color` uniform within the fragment shader.


.. code:: python
          
   quad['position'] = [(-0.5, -0.5),
                       (-0.5, +0.5),
                       (+0.5, -0.5),
                       (+0.5, +0.5)]
   quad['color'] = 0,0,0,1

Last, we specify in the :meth:`~glumpy.app.Window.on_draw` method that the quad
needs to be rendered using :const:`gl.GL_TRIANGLE_STRIP`.

.. code:: python

   @window.event
   def on_draw(dt):
       window.clear()
       quad.draw(gl.GL_TRIANGLE_STRIP)

   app.run()
   

Animating shapes
================

Animation is just a matter of modifying what is drawn at each time step. We'll
use the example above in order to make the quad to grow and shrinks with
time. First things is to keep track of time using the prodived ``dt`` parameter
in the :meth:`~glumpy.app.Window.on_draw` function that give the elapsed time
since last call. We'll first add a new uniform in the vertex shader source code
and adapt quad coordinates according to the sine of the time variable.

.. code:: C

   vertex = """
            uniform float time;
            vec2 attribute position;
            void main()
            {
                vec2 xy = vec2(sin(2.0*time));
                gl_Position = vec4(position*(0.25 + 0.75*xy*xy), 0.0, 1.0);
            } """

We also need to initialize the time variable and to update it at each draw
call.
            
.. code:: python
          
   @window.event
   def on_draw(dt):
       window.clear()
       quad["time"] += dt
       quad.draw(gl.GL_TRIANGLE_STRIP)

   quad["time"] = 0.0
   quad['color'] = 1,0,0,1
   quad['position'] = [(-1, -1), (-1, +1), (+1, -1), (+1, +1)]
   app.run()

.. note::

   If you want to record the animation you can use the ``--record filename``
   switch when starting your application.


..
   ==========
   Quickstart
   ==========

   Hello World!
   ============

   This program opens a window with black background and wait for it to be closed
   by the user (by clicking the close button or pressing the escape key):

   .. code:: python

      from glumpy import app

      window = app.Window()
      @window.event
      def on_draw(dt):
          window.clear()
      app.run()


   .. note:: The **run** method only returns when all application windows have
             been closed unless the program has been launched in **interactive
             mode.** If you start the program using the ``--interactive`` switch,
             the `app.run()` is no londer blocking:

             .. code::

                $ python app-simple.py -i
                [i] HiDPI detected, fixing window size
                [i] Using GLFW (GL 2.1)
                [i] Running at 60 frames/second
                >>> window.clear = 1,1,1,1

             The window should be now white instead of black.


   Hello Open GL!
   ==============

   Glumpy offers an easy access to modern OpenGL (i.e. shaders and programs) and
   the program below shows the most straightforward way to write a program using
   both a vertex and a fragment shader.

   .. code:: python

      from glumpy import app, gloo, gl

      vertex = """
             vec2 attribute position;
             void main()
             {
                 gl_Position = vec4(position, 0.0, 1.0);
             } """

      fragment = """
             uniform vec4 color;
             void main() {
                 gl_FragColor = color;
             } """

      window = app.Window()
      quad = gloo.Program(vertex, fragment, 4)
      quad['position'] = [(-1, -1), (-1, +1), (+1, -1), (+1, +1)]
      quad['color'] = 0,0,0,1

      @window.event
      def on_draw(dt):
          window.clear()
          quad.draw(gl.GL_TRIANGLES)

      app.run()


   ..
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




      ..
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
         screen. However

         the real power of modern OpenGL lies in the possibility of
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
