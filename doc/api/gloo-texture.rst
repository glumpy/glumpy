.. ----------------------------------------------------------------------------
.. _textures-section:

========
Textures
========

.. automodule:: glumpy.gloo.texture

**Content**

* :any:`texture-section`          — Generic texture methods
* :any:`texture-1d-section`       — One dimensional texture
* :any:`texture-float-1d-section` — One dimensional float texture
* :any:`texture-2d-section`       — Two dimensional texture
* :any:`texture-float-2d-section` — Two dimensional float texture
* :any:`texture-atlas-section`    — Two dimensional texture atlas
* :any:`depth-texture-section`    — Depth texture
* :any:`texture-cube-section`     — Texture cube

  
.. ----------------------------------------------------------------------------
.. _texture-section:

Texture
=======

.. autoclass:: glumpy.gloo.Texture
   :show-inheritance:
   :members: cpu_format, gpu_format, interpolation, wrapping

             
.. ----------------------------------------------------------------------------
.. _texture-1d-section:

Texture1D
=========

.. autoclass:: glumpy.gloo.Texture1D
   :show-inheritance:
   :members: width


.. ----------------------------------------------------------------------------
.. _texture-float-1d-section:

TextureFloat1D
==============

.. autoclass:: glumpy.gloo.TextureFloat1D
   :show-inheritance:
   :members: width

             
.. ----------------------------------------------------------------------------
.. _texture-2d-section:

Texture2D
=========

.. autoclass:: glumpy.gloo.Texture2D
   :show-inheritance:
   :members:


.. ----------------------------------------------------------------------------
.. _texture-float-2d-section:

TextureFloat2D
==============
      
.. autoclass:: glumpy.gloo.TextureFloat2D
   :show-inheritance:
   :members:

      
.. ----------------------------------------------------------------------------
.. _texture-atlas-section:

TextureAtlas
============

.. autoclass:: glumpy.gloo.Atlas
   :show-inheritance:


.. ----------------------------------------------------------------------------
.. _depth-texture-section:

DepthTexture
============
      
.. autoclass:: glumpy.gloo.DepthTexture
   :show-inheritance:
   :members:


.. ----------------------------------------------------------------------------
.. _texture-cube-section:

TextureCube
===========

.. autoclass:: glumpy.gloo.TextureCube
   :show-inheritance:
   :members:

