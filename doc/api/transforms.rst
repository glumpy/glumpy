.. ----------------------------------------------------------------------------
.. _section-transforms:

==========
Transforms
==========

The ``glumpy.transforms`` module offers common transforms (interactive or not).

* **Base**

  * :any:`transform-transform`   — Base transform
  * :any:`transform-viewport`    — Viewport transformation and clipping
  * :any:`transform-position`    — Generic position transform
  * :any:`transform-translate`   — Translate transform
  * :any:`transform-rotate`      — Rotate transform
    
* **Interactive**
  
  * :any:`transform-panzoom`     — User controlled pan & zoom (2D)
  * :any:`transform-trackball`   — User controlled trackball (3D)

* **Scale**

  * :any:`transform-quantitative-scale`  — Quantitative scale (base)
  * :any:`transform-linear-scale`        — Linear scale
  * :any:`transform-power-scale`         — Power scale
  * :any:`transform-log-scale`           — Log scale
      
* **Projection**

  * :any:`transform-orthographic` — Orthographic projection
  * :any:`transform-perpsective`  — Perspective projection
  * :any:`transform-pvm`          — Model-View-Projection model
  
* **Cartographic**

  * :any:`transform-conic-equal-area`      — Conic Equal Area
  * :any:`transform-azimuthal-equal-area`  — Azimuthal Equal Area
  * :any:`transform-azimuthal-equidistant` — Azimuthal Equidistant
  * :any:`transform-albers` — Conic Equal Area, with USA-centric defaults

    
.. ----------------------------------------------------------------------------
.. toctree::
   :hidden:

   transform-panzoom
   transform-trackball
   transform-viewport
   transform-position
   transform-translate
   transform-rotate
