.. _gloo-quad.py:            https://github.com/glumpy/glumpy/blob/master/examples/gloo-quad.py
.. _gloo-cube.py:            https://github.com/glumpy/glumpy/blob/master/examples/gloo-cube.py
.. _gloo-texture-1D.py:      https://github.com/glumpy/glumpy/blob/master/examples/gloo-texture-1D.py
.. _gloo-texture-2D.py:      https://github.com/glumpy/glumpy/blob/master/examples/gloo-texture-2D.py
.. _gloo-image.py:           https://github.com/glumpy/glumpy/blob/master/examples/gloo-image.py
.. _gloo-console.py:         https://github.com/glumpy/glumpy/blob/master/examples/gloo-console.py
.. _gloo-cloud.py:           https://github.com/glumpy/glumpy/blob/master/examples/gloo-cloud.py
.. _gloo-terminal.py:        https://github.com/glumpy/glumpy/blob/master/examples/gloo-terminal.py
.. _gloo-atlas.py:           https://github.com/glumpy/glumpy/blob/master/examples/gloo-atlas.py
.. _gloo-framebuffer.py:     https://github.com/glumpy/glumpy/blob/master/examples/gloo-framebuffer.py
.. _gloo-rain.py:            https://github.com/glumpy/glumpy/blob/master/examples/gloo-rain.py
.. _gloo-trail.py:           https://github.com/glumpy/glumpy/blob/master/examples/gloo-trail.py
.. _gloo-arrows.py:          https://github.com/glumpy/glumpy/blob/master/examples/gloo-arrows.py
.. _gloo-marker.py:          https://github.com/glumpy/glumpy/blob/master/examples/gloo-marker.py
.. _gloo-antialias.py:       https://github.com/glumpy/glumpy/blob/master/examples/gloo-antialias.py
.. _gloo-picking.py:         https://github.com/glumpy/glumpy/blob/master/examples/gloo-picking.py
.. _gloo-trace.py:           https://github.com/glumpy/glumpy/blob/master/examples/gloo-trace.py
.. _gloo-magnify.py:         https://github.com/glumpy/glumpy/blob/master/examples/gloo-magnify.py

.. _gloo-cartesian-grid.py:  https://github.com/glumpy/glumpy/blob/master/examples/gloo-cartesian-grid.py
.. _gloo-hexagonal-grid.py:  https://github.com/glumpy/glumpy/blob/master/examples/gloo-hexagonal-grid.py
.. _gloo-irregular-grids.py: https://github.com/glumpy/glumpy/blob/master/examples/gloo-irregular-grids.py
.. _gloo-triangular-grid.py: https://github.com/glumpy/glumpy/blob/master/examples/gloo-triangular-grid.py
.. _gloo-regular-grids.py:   https://github.com/glumpy/glumpy/blob/master/examples/gloo-regular-grids.py
.. _gloo-frame.py:           https://github.com/glumpy/glumpy/blob/master/examples/gloo-frame.py
.. _gloo-transparency.py:    https://github.com/glumpy/glumpy/blob/master/examples/gloo-transparency.py

.. ----------------------------------------------------------------------------
.. _section-examples-gloo:

============
OpenGL layer
============

The ``glumpy.gloo`` layer is the heart of glumpy and is responsible for talking
to the GPU throught buffers, textures and programs. This is done quite
transparently thanks to the numpy interface (and the GPU data object which is a
subclassed numpy array).


* gloo-quad.py_
    This example displays a simple yellow quad.

* gloo-cube.py_
    This example shows a rotating, colored & outlined cube. It uses transformation
    matrices to translate, rotate and finally project the cube on the window framebuffer.
    
    .. note::

       Note that there are easier ways to do the same using transforms.

* gloo-texture-1D.py_
    This example shows how to upload and display a 1-dimensional texture.

* gloo-texture-2D.py_
    This example shows how to upload and display a 2-dimensional texture.

* gloo-image.py_
    This examples shows how to display an image, without control of the aspect ratio though.

    .. warning::

       This example does not enforce image aspect ratio when window size is changed.

* gloo-console.py_
    This examples show how to use the on-screen console that should never fails.

    .. note::

       The console is fairly limited and must be used for debugging purposes only.

* gloo-terminal.py_
    This examples show a more complete terminal that is able to scroll and to
    display an extended set of characters (just scroll to see them). It is very
    fast and can be used for quick'n'dirty input/output.

    .. note::

       The terminal uses a dedicated technique to ensure rendering speed. For
       better text output, one must used a glyph collection.
       
* gloo-atlas.py_
    This example shows how to use a texture atlas object that allow to store
    different texture into a single one.
    
* gloo-framebuffer.py_
    This examples shows how to used the framebuffer. The scene is first
    rendered into a texture using ut-of bound color values (10) and the
    resulting texture is displayed on screen and correct the color value such
    as to display a gray quad.
  
* gloo-cloud.py_
    This example shows a rotating 3d scatter plots made of a million antialiased
    points. It should run smoothly on any recent hardware.

* gloo-antialias.py_
    This example illustrates stroke, filled and outline antialiased shaders that are used
    in a number of different places throughout glumpy.

* gloo-arrows.py_
    This is an example of what can be done using dedicated shaders. In this
    example, each arrow is a point but is draw as an antialiased arrow in the
    fragment shader using signed distance field.

    .. note::
       
       You can read more on these techniques in this `article
       <http://jcgt.org/published/0003/04/01/>`_ of the Journal of Graphics
       Techniques (which is also a good source of knowledge).

* gloo-marker.py_
    This example show various antialiased markers made using signed-distance
    functions.

* gloo-magnify.py_
    This examples displays a 2D scatter plot and is zoomed dynamically around
    the mouse pointer thanks to the shaders.

* gloo-rain.py_
    This example simulates rain drops using growing and fading circles and
    shows how to update a vertex buffer.

* gloo-trail.py_
    This example shows mouse trails using growing and fadind discs. It
    illustrate how to use mouse interactions to update a vertex buffer.

* gloo-picking.py_
    This example show how to perform object picking using colors. When pick
    mode is active (mouse press), each object is rendered using a unique color
    and the color under the mouse is used to compute the object id.
    
* gloo-trace.py_
    This example displays several signals that slowly fade out. The trick is to
    not clear the framebuffer and to draw a quasi transparent quad over the
    whole scene, making older signals to slowly vanish.

