.. ----------------------------------------------------------------------------
.. _section-transforms:

===============
Transformations
===============

The ``glumpy.transforms`` module offers common transforms (interactive or not)
that can be combined with other shaders and objects, espcially collections.


.. warning::

   In all transforms, parameters must be passed by name (param=value) because
   positional arguments are reserved for the super class (Snippet).

   A transform must be attached to a window such as to receive user events.



* :any:`section-transform-base`

  * :any:`transform-transform`  - General base transform
  * :any:`transform-viewport`   — Viewport transformation and clipping
  * :any:`transform-position`   — Generic position transform
  * :any:`transform-translate`  — Translate transform
  * :any:`transform-rotate`     — Rotate transform
    
* :any:`section-transform-interactive`

  * :any:`transform-panzoom`           — User controlled pan & zoom (2D)
  * :any:`transform-trackball`         — User controlled trackball (3D)

* :any:`section-transform-scale`

  * :any:`transform-quantitative-scale` — Quantitative scale

    * :any:`transform-linear-scale`       — Linear scale
    * :any:`transform-power-scale`        — Power scale
    * :any:`transform-log-scale`          — Log scale

* :any:`section-transform-projection`

  * :any:`transform-orthographic`     — Orthographic projection
  * :any:`transform-pvm`              — Perspective projection
    
* :any:`section-transform-cartographic`

  * :any:`transform-conic-equal-area`      — Conic Equal Area
  * :any:`transform-albers`                — Albers
  * :any:`transform-azimuthal-equal-area`  — Azimuthal Equal Area
  * :any:`transform-azimuthal-equidistant` — Azimuthal Equidistant

    
.. ----------------------------------------------------------------------------
.. toctree::
   :hidden:

   transform-base
   transform-interactive
   transform-scale
   transform-projection
   transform-cartographic

