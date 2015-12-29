.. _transform-pan-zoom.py:      https://github.com/glumpy/glumpy/blob/master/examples/transform-pan-zoom.py
.. _transform-trackball.py:     https://github.com/glumpy/glumpy/blob/master/examples/transform-trackball.py
.. _transform-pvm.py:           https://github.com/glumpy/glumpy/blob/master/examples/transform-pvm.py
.. _transform-ortho.py:         https://github.com/glumpy/glumpy/blob/master/examples/transform-ortho.py
.. _transform-image.py:         https://github.com/glumpy/glumpy/blob/master/examples/transform-image.py
.. _transform-rotate.py:        https://github.com/glumpy/glumpy/blob/master/examples/transform-rotate.py
.. _transform-polar.py:         https://github.com/glumpy/glumpy/blob/master/examples/transform-polar.py
.. _transform-linear-scale.py:  https://github.com/glumpy/glumpy/blob/master/examples/transform-linear-scale.py
.. _transform-log-scale.py:     https://github.com/glumpy/glumpy/blob/master/examples/transform-log-scale.py
.. _transform-power-scale.py:   https://github.com/glumpy/glumpy/blob/master/examples/transform-power-scale.py
.. _transform-lin-log-scale.py: https://github.com/glumpy/glumpy/blob/master/examples/transform-linear-log-scale.py
.. _transform-log-polar.py: https://github.com/glumpy/glumpy/blob/master/examples/transform-log-polar.py

.. ----------------------------------------------------------------------------
.. _section-examples-transform:

==========
Transforms
==========

Transforms are snippets that can be attached to events (resize, mouse_scroll,
etc.) and inserted into other shader code using hooks.

* transform-pvm.py_
    This example shows a simple Projection/Model/View transform that is
    equivalent to the deprecated GL API (1.0).

* transform-pan-zoom.py_
    The panzoom transform allow to translate and scale an object in the window
    space coordinate (2D).

* transform-trackball.py_
    The trackball transform simulates a virtual trackball (3D) that can rotate
    around the origin using intuitive mouse gestures.

* transform-ortho.py_
    This examples shows and orthographic projection where coordinates are
    manipulated in pixels.

* transform-rotate.py_
    This example shows a simple rotating quad using the ``Rotate`` transform.
   

* transform-linear-scale.py_
    Simple linear scale that maps point from a domain to a given range.

* transform-power-scale.py_
    Power scales are similar to linear scales, except there's an exponential
    transform that is applied to the input domain value before the output range
    value is computed.

* transform-log-scale.py_
    Log scales are similar to linear scales, except there's a logarithmic
    transform that is applied to the input domain value before the output range
    value is computed.

* transform-lin-log-scale.py_
    This example show how to use different scales on x, y, or z.

* transform-polar.py_
    Simple polar projection.

* transform-log-polar.py_
    Simple composition of a polar projection and a log scale on the radius.
