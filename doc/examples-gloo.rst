.. _gloo-quad.py:            https://github.com/glumpy/glumpy/blob/master/examples/gloo-quad.py
.. _gloo-cube.py:            https://github.com/glumpy/glumpy/blob/master/examples/gloo-cube.py
.. _gloo-texture-1D.py:      https://github.com/glumpy/glumpy/blob/master/examples/gloo-texture-1D.py
.. _gloo-texture-2D.py:      https://github.com/glumpy/glumpy/blob/master/examples/gloo-texture-2D.py
.. _gloo-lena.py:            https://github.com/glumpy/glumpy/blob/master/examples/gloo-lena.py
.. _gloo-console.py:         https://github.com/glumpy/glumpy/blob/master/examples/gloo-console.py
.. _gloo-terminal.py:        https://github.com/glumpy/glumpy/blob/master/examples/gloo-terminal.py
.. _gloo-cloud.py:           https://github.com/glumpy/glumpy/blob/master/examples/gloo-cloud.py
.. _gloo-atlas.py:           https://github.com/glumpy/glumpy/blob/master/examples/gloo-atlas.py
.. _gloo-framebuffer.py:     https://github.com/glumpy/glumpy/blob/master/examples/gloo-framebuffer.py
.. _gloo-rain.py:            https://github.com/glumpy/glumpy/blob/master/examples/gloo-rain.py
.. _gloo-trail.py:           https://github.com/glumpy/glumpy/blob/master/examples/gloo-trail.py
.. _gloo-arrows.py:          https://github.com/glumpy/glumpy/blob/master/examples/gloo-arrows.py
.. _gloo-marker.py:          https://github.com/glumpy/glumpy/blob/master/examples/gloo-marker.py
.. _gloo-antialias.py:       https://github.com/glumpy/glumpy/blob/master/examples/gloo-antialias.py
.. _gloo-picking.py:         https://github.com/glumpy/glumpy/blob/master/examples/gloo-picking.py

.. _gloo-cartesian-grid.py:  https://github.com/glumpy/glumpy/blob/master/examples/gloo-cartesian-grid.py
.. _gloo-hexagonal-grid.py:  https://github.com/glumpy/glumpy/blob/master/examples/gloo-hexagonal-grid.py
.. _gloo-irregular-grids.py: https://github.com/glumpy/glumpy/blob/master/examples/gloo-irregular-grids.py
.. _gloo-triangular-grid.py: https://github.com/glumpy/glumpy/blob/master/examples/gloo-triangular-grid.py
.. _gloo-regular-grids.py:   https://github.com/glumpy/glumpy/blob/master/examples/gloo-regular-grids.py
.. _gloo-frame.py:           https://github.com/glumpy/glumpy/blob/master/examples/gloo-frame.py

.. _gloo-magnify.py:         https://github.com/glumpy/glumpy/blob/master/examples/gloo-magnify.py
.. _gloo-pulsing-quad.py:    https://github.com/glumpy/glumpy/blob/master/examples/gloo-pulsing-quad.py
.. _gloo-trace.py:           https://github.com/glumpy/glumpy/blob/master/examples/gloo-trace.py
.. _gloo-transparency.py:    https://github.com/glumpy/glumpy/blob/master/examples/gloo-transparency.py

=======================
OpenGL Object interface
=======================

The ``glumpy.gloo`` layer is the heart of glumpy and is responsible for talking
to the GPU throught buffers, textures and programs. This is done quite
transparently thanks to the numpy interface (and the GPU data object which is a
subclassed numpy array).


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



