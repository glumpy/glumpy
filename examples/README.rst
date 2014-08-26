========
Examples
========

App
===

**glumpy.app** is the layer responsible for opening a window, handling events
(mouse, keyboard and user event). It also provides convenient interfaces to
parse command line options and configure the GL context.

* `app-simple.py <https://github.com/rougier/glumpy/blob/master/examples/app-simple.py>`_

  The most simple glumpy example. This should display a black window.

* `app-config.py <https://github.com/rougier/glumpy/blob/master/examples/app-config.py>`_

  This shows how to setup a specific GL configuration (depth buffer size, stencil, ...)

* `app-events.py <https://github.com/rougier/glumpy/blob/master/examples/app-events.py>`_

  This example connect to all available events and display them when triggered.

* `app-screenshot.py <https://github.com/rougier/glumpy/blob/master/examples/app-screenshot.py>`_

  This takes a screenshot and exit.

* `app-timed.py <https://github.com/rougier/glumpy/blob/master/examples/app-timed.py>`_

  Open a window, display it for 1 second and exit.

* `app-two-windows.py <https://github.com/rougier/glumpy/blob/master/examples/app-two-windows.py>`_

  Open two windows, one black, one white.

* `app-two-programs.py <https://github.com/rougier/glumpy/blob/master/examples/app-two-programs.py>`_

  Display two points (square), one blue, one red.

* `app-event-loop.py <https://github.com/rougier/glumpy/blob/master/examples/app-event-loop.py>`_

  Show how to manually handle the event loop.

* `app-interactive.py <https://github.com/rougier/glumpy/blob/master/examples/app-interactive.py>`_

  Display a window in interactive mode (python console is reactive).



Gloo
====

**glumpy.gloo** is the heart of glumpy and is responsible for talking to the
GPU throught buffers, textures and programs. This is done quite transparently
thanls to the numpy interface (and the GPU data object which is a subclassed
numpy array).


* `gloo-quad.py <https://github.com/rougier/glumpy/blob/master/examples/gloo-quad.py>`_

  This example shows an animated colored quad made of two triangles in orthographic mode.

  .. image:: https://raw.githubusercontent.com/rougier/glumpy/master/doc/_static/screenshots/gloo-quad.png


* `gloo-cube.py <https://github.com/rougier/glumpy/blob/master/examples/gloo-cube.py>`_

  This example shows a rotating, colored & outlined cube. It uses transformation
  matrices to translate, rotate and finally project the cube on the window framebuffer.

  .. image:: https://raw.githubusercontent.com/rougier/glumpy/master/doc/_static/screenshots/gloo-cube.png


* `gloo-texture-1D.py <https://github.com/rougier/glumpy/blob/master/examples/gloo-texture-1D.py>`_

  This example shows how to manipulate 1-dimensional textures.

  .. image:: https://raw.githubusercontent.com/rougier/glumpy/master/doc/_static/screenshots/gloo-texture-1D.png


* `gloo-texture-2D.py <https://github.com/rougier/glumpy/blob/master/examples/gloo-texture-2D.py>`_

  This example shows how to manipulate 2-dimensional textures.

  .. image:: https://raw.githubusercontent.com/rougier/glumpy/master/doc/_static/screenshots/gloo-texture-2D.png


* `gloo-lena.py <https://github.com/rougier/glumpy/blob/master/examples/gloo-lena.py>`_

  This examples shows how to display an image, without control of the aspect ratio though.

  .. image:: https://raw.githubusercontent.com/rougier/glumpy/master/doc/_static/screenshots/gloo-lena.png


* `gloo-console.py <https://github.com/rougier/glumpy/blob/master/examples/gloo-console.py>`_

  This examples shows how to invoke a (simple) console to display information.

  .. image:: https://raw.githubusercontent.com/rougier/glumpy/master/doc/_static/screenshots/gloo-console.png


* `gloo-rain.py <https://github.com/rougier/glumpy/blob/master/examples/gloo-rain.py>`_

  This example simulates rain drops using growing and fading circles and shows how to update a vertex buffer.

  .. image:: https://raw.githubusercontent.com/rougier/glumpy/master/doc/_static/screenshots/gloo-rain.png


* `gloo-trail.py <https://github.com/rougier/glumpy/blob/master/examples/gloo-trail.py>`_

* `gloo-atlas.py <https://github.com/rougier/glumpy/blob/master/examples/gloo-atlas.py>`_

* `gloo-quiver.py <https://github.com/rougier/glumpy/blob/master/examples/gloo-quiver.py>`_

* `gloo-cloud.py <https://github.com/rougier/glumpy/blob/master/examples/gloo-cloud.py>`_

* `gloo-marker.py <https://github.com/rougier/glumpy/blob/master/examples/gloo-marker.py>`_

  This example show various antialiased markers. The anti-aliasing is computed
  by the GPU using signed-distance functions that describe the mathematical
  shape. This makes the display very fast (it is possible to display a million
  points this way, provided they're not too big in terms of pixels area).

  .. image:: https://raw.githubusercontent.com/rougier/glumpy/master/doc/_static/screenshots/gloo-marker.png




..
   ` <https://github.com/rougier/glumpy/blob/master/examples/>`_
   ` <https://github.com/rougier/glumpy/blob/master/examples/>`_
   ` <https://github.com/rougier/glumpy/blob/master/examples/>`_
   ` <https://github.com/rougier/glumpy/blob/master/examples/>`_
   gloo-arrows.py
   gloo-solid-segment.py
   gloo-voronoi.py
   gloo-frame.py
   gloo-terminal.py
   gloo-cartesian-grid.py
   gloo-hexagonal-grid.py
   gloo-irregular-grids.py
   gloo-regular-grids.py
