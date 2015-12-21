==========
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
