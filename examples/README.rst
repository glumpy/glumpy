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

  This example connects to all available events and display them when triggered.

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


* `gloo-quad.py
  <https://github.com/rougier/glumpy/blob/master/examples/gloo-quad.py>`_ shows
  an animated colored quad made of two triangles in orthographic mode.


* `gloo-cube.py
  <https://github.com/rougier/glumpy/blob/master/examples/gloo-cube.py>`_ shows
  a rotating, colored & outlined cube. It uses transformation matrices to
  translate, rotate and finally project the cube on the window framebuffer.


* `gloo-texture-1D.py
  <https://github.com/rougier/glumpy/blob/master/examples/gloo-texture-1D.py>`_
  shows how to manipulate 1-dimensional textures.


* `gloo-texture-2D.py
  <https://github.com/rougier/glumpy/blob/master/examples/gloo-texture-2D.py>`_ shows
  how to manipulate 2-dimensional textures.


* `gloo-lena.py
  <https://github.com/rougier/glumpy/blob/master/examples/gloo-lena.py>`_ shows
  how to display an image, without control of the aspect ratio though.


* `gloo-console.py
  <https://github.com/rougier/glumpy/blob/master/examples/gloo-console.py>`_
  shows how to invoke a (simple) console to display information.


* `gloo-rain.py
  <https://github.com/rougier/glumpy/blob/master/examples/gloo-rain.py>`_
  simulates rain drops using growing and fading circles and shows how to update
  a vertex buffer.


* `gloo-trail.py
  <https://github.com/rougier/glumpy/blob/master/examples/gloo-trail.py>`_
  shows mouse trails using growing and fadind discs. It illustrate how to use
  mouse interation to update a vertex buffer.


* `gloo-atlas.py
  <https://github.com/rougier/glumpy/blob/master/examples/gloo-atlas.py>`_
  illustrates the atlas object that allow to store different texture into a
  single one.


* `gloo-marker.py
  <https://github.com/rougier/glumpy/blob/master/examples/gloo-marker.py>`_
  shows various antialiased markers. The anti-aliasing is computed by the GPU
  using signed-distance functions that describe the mathematical shape. This
  makes the display very fast (it is possible to display a million points this
  way, provided they're not too big in terms of pixels area).


* `gloo-cloud.py
  <https://github.com/rougier/glumpy/blob/master/examples/gloo-cloud.py>`_
  shows an animated 3d scatter plots made of a million antialiased points. It
  should run smoothly on any recent hardware.



Computation
===========

* Game of life
* Grayscott Reaction-Diffusion system


Post-processing filters
=======================

* Sepia colors
* Gaussian blur
* Filter composition


Snippets
========

* 2D plots on regular grid
* 3D plots on regular grid
* Arbitrary viewports


Transforms
==========

* Pan-zoom
* Trackball
* Projection / Model / View


Eye-candy demonstrations
========================

* Spiral galaxy
* Fireworks
* Voronoi
* Quiver plot
* Realtime signals


Collections
===========

* Points
* Lines
* Triangles
* Markers
* Antialiased solid lines
* Antialiased dashed lines


Technics
========

* Read movie
* Write movie
* Antialiased grids
* Heighfields
* High-frequency signal
* Image spatial interpolations
