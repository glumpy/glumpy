========
Examples
========

App
===

**glumpy.app** is the layer responsible for opening a window, handling events
(mouse, keyboard and user event). It also provides convenient interfaces to
parse command line options and configure the GL context.

* `app-backend.py <https://github.com/glumpy/glumpy/blob/master/examples/app-backend.py>`_

  Show how to change the backend programatically.


* `app-config.py <https://github.com/glumpy/glumpy/blob/master/examples/app-config.py>`_

  This shows how to setup a specific GL configuration (depth buffer size, stencil, ...)


* `app-event-loop.py <https://github.com/glumpy/glumpy/blob/master/examples/app-event-loop.py>`_

  Show how to manually handle the event loop.


* `app-events.py <https://github.com/glumpy/glumpy/blob/master/examples/app-events.py>`_

  This example connect to all available events and display them when triggered.


* `app-interactive.py <https://github.com/glumpy/glumpy/blob/master/examples/app-interactive.py>`_

  Display a window in interactive mode (python console is reactive).


* `app-screenshot.py <https://github.com/glumpy/glumpy/blob/master/examples/app-screenshot.py>`_

  This takes a screenshot and exit.


* `app-simple.py <https://github.com/glumpy/glumpy/blob/master/examples/app-simple.py>`_

  The most simple glumpy example. This should display a black window.


* `app-timed.py <https://github.com/glumpy/glumpy/blob/master/examples/app-timed.py>`_

  Open a window, display it for 1 second and exit.


* `app-two-windows.py <https://github.com/glumpy/glumpy/blob/master/examples/app-two-windows.py>`_

  Open two windows, one black, one white.


* `app-two-programs.py <https://github.com/glumpy/glumpy/blob/master/examples/app-two-programs.py>`_

  Display two points (square), one blue, one red.




Gloo
====

**glumpy.gloo** is the heart of glumpy and is responsible for talking to the
GPU throught buffers, textures and programs. This is done quite transparently
thanks to the numpy interface (and the GPU data object which is a subclassed
numpy array).


* `gloo-antialias.py <https://github.com/glumpy/glumpy/blob/master/examples/gloo-antialias.py>`_

  This example shows stroke, filled and outline antialiased shader.


* `gloo-arrows.py <https://github.com/glumpy/glumpy/blob/master/examples/gloo-arrows.py>`_

  This example shows antialiased arrows using points.


* `gloo-atlas.py <https://github.com/glumpy/glumpy/blob/master/examples/gloo-atlas.py>`_

  This example illustrates the atlas object that allow to store different
  texture into a single one.


* `gloo-cloud.py <https://github.com/glumpy/glumpy/blob/master/examples/gloo-cloud.py>`_

  This example show an animated 3d scatter plots made of a million antialiased
  points. It should run smoothly on any recent hardware.


* `gloo-console.py <https://github.com/glumpy/glumpy/blob/master/examples/gloo-console.py>`_

  This is a failsafe debug console that should never fails...


* `gloo-cube.py <https://github.com/glumpy/glumpy/blob/master/examples/gloo-cube.py>`_

  This example shows a rotating, colored & outlined cube. It uses transformation
  matrices to translate, rotate and finally project the cube on the window framebuffer.
  Note that there are easier way to do the same with glumpy (transforms).


* `gloo-lena.py <https://github.com/glumpy/glumpy/blob/master/examples/gloo-lena.py>`_

  This examples shows how to display an image, without control of the aspect ratio though.


* `gloo-magnify.py <https://github.com/glumpy/glumpy/blob/master/examples/gloo-magnify.py>`_

  This examples shows a scatter plot which is zoomed dynamically around the mouse pointer.


* `gloo-marker.py <https://github.com/glumpy/glumpy/blob/master/examples/gloo-marker.py>`_

  This example show various antialiased markers. The anti-aliasing is computed
  by the GPU using signed-distance functions that describe the mathematical
  shape. This makes the display very fast (it is possible to display a million
  points this way, provided they're not too big in terms of pixels area).


* `gloo-quad.py <https://github.com/glumpy/glumpy/blob/master/examples/gloo-quad.py>`_

  This example shows an animated colored quad made of two triangles in orthographic mode.


* `gloo-rain.py <https://github.com/glumpy/glumpy/blob/master/examples/gloo-rain.py>`_

  This example simulates rain drops using growing and fading circles and shows
  how to update a vertex buffer.


* `gloo-texture-1D.py <https://github.com/glumpy/glumpy/blob/master/examples/gloo-texture-1D.py>`_

  This example shows how to manipulate 1-dimensional textures.


* `gloo-texture-2D.py <https://github.com/glumpy/glumpy/blob/master/examples/gloo-texture-2D.py>`_

  This example shows how to manipulate 2-dimensional textures.


* `gloo-trace.py <https://github.com/glumpy/glumpy/blob/master/examples/gloo-trace.py>`_

  This example display a bunch of signals that slowly fades out. The tick is to
  not clear the framebuffer but to draw a almost transparent quad over the
  scene, making older signals to slowly vanish.


* `gloo-trail.py <https://github.com/glumpy/glumpy/blob/master/examples/gloo-trail.py>`_

  This example show mouse trails using growing and fadind discs. It illustrate how to use
  mouse interation to update a vertex buffer.




Computation
===========

Simple computation can be directly written using the GPU (no Cuda, no OpenCL):


* `game-of-life.py <https://github.com/glumpy/glumpy/blob/master/examples/game-of-life.py>`_

  This is the Game Of Life computed on the GPU (very fast).

* `grayscott.py <https://github.com/glumpy/glumpy/blob/master/examples/grayscott.py>`_

  This is a Grayscott Reaction-Diffusion system.


* `smoke.py <https://github.com/glumpy/glumpy/blob/master/examples/smoke/smoke.py>`_

  This is smoke simulation ported from the `little grasshopper <http://prideout.net/blog/?p=58>`_.



Post-processing filters
=======================

Post-processing filters are easily implemented using the Filter object. You
draw tour scene normally but the draw calls are surrounded by a ```with
Filter(shader)`` where the shader transform the otuput.

* `filter-pixelate.py <https://github.com/glumpy/glumpy/blob/master/examples/filter-sepia.py>`_

  Pixelating filter with pixelation level controlled by mouse scroll.


* `filter-blur.py <https://github.com/glumpy/glumpy/blob/master/examples/filter-blur.py>`_

  Simple 2D Gaussian blur using two 1D kernels.


* `filter-composition.py <https://github.com/glumpy/glumpy/blob/master/examples/filter-composition.py>`_

  This example show how to compose filters together.



Snippets
========

* 2D plots on regular grid
* 3D plots on regular grid
* Arbitrary viewports


Transforms
==========

Transforms are snippets that can be attached to events (resize, mouse_scroll,
etc.) and inserted into other shader code using hooks.

* `transform-pan-zoom.py <https://github.com/glumpy/glumpy/blob/master/examples/transform-pan-zoom.py>`_

  The panzoom transform allow to translate and scale an object in the window
  space coordinate (2D).


* `transform-trackball.py <https://github.com/glumpy/glumpy/blob/master/examples/transform-trackball.py>`_

  The trackball transform simulates a virtual trackball (3D) that can rotate
  around the origin using intuitive mouse gestures.


* `transform-pvm.py <https://github.com/glumpy/glumpy/blob/master/examples/transform-pvm.py>`_

  Projection / Model / View transform (equivalen to the deprecated GL api)


* `transform-ortho.py <https://github.com/glumpy/glumpy/blob/master/examples/transform-ortho.py>`_

  The orthographic projection can be combined with the panzoom tranform.


* `transform-linear-scale.py <https://github.com/glumpy/glumpy/blob/master/examples/transform-linear-scale.py>`_

  Simple linear scale that maps point from a domain to a given range.

* `transform-power-scale.py <https://github.com/glumpy/glumpy/blob/master/examples/transform-power-scale.py>`_

  Power scales are similar to linear scales, except there's an exponential
  transform that is applied to the input domain value before the output range
  value is computed.

* `transform-log-scale.py <https://github.com/glumpy/glumpy/blob/master/examples/transform-log-scale.py>`_

  Log scales are similar to linear scales, except there's a logarithmic
  transform that is applied to the input domain value before the output range
  value is computed.

* `transform-lin-log-scale.py <https://github.com/glumpy/glumpy/blob/master/examples/transform-linear-log-scale.py>`_

  This example show how to use different scales on x, y, or z.

* `transform-polar.py <https://github.com/glumpy/glumpy/blob/master/examples/transform-polar.py>`_

  Simple polar projection.

* `transform-log-polar.py <https://github.com/glumpy/glumpy/blob/master/examples/transform-log-polar.py>`_

  Simple composition of a polar projection and a log scale on the radius.




Eye-candy demonstrations
========================

* Spiral galaxy
* Fireworks
* Voronoi
* Quiver plot
* Realtime signals
* Tiger


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
