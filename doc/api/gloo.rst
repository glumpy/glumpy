===================
OpenGL layer (gloo)
===================

The ``glumpy.gloo`` module offers an intuitive interface to modern OpenGL
through buffers, textures and programs.

* :any:`globject-section`            — Base class for all GPU objects
* :any:`gpudata-section`             — Memory tracked numpy array
* :any:`shaders-section`

  * :any:`program-section`         — Shader program
  * :any:`shader-section`          — Generic shader methods
  * :any:`vertex-shader-section`   — Vertex shader
  * :any:`fragment-shader-section` — Fragment shader
  * :any:`geometry-shader-section` — Geometry shader

* :any:`buffers-section`
  
  * :any:`buffer-section`        — Generic buffer methods
  * :any:`vertex-buffer-section` — Vertex buffer
  * :any:`index-buffer-section`  — Index buffer

* :any:`textures-section`

  * :any:`texture-section`           — Generic texture methods
  * :any:`texture-1d-section`        — One dimensional texture
  * :any:`texture-float-1d-section`  — One dimensional float texture
  * :any:`texture-2d-section`        — Two dimensional texture
  * :any:`texture-float-2d-section`  — Two dimensional float texture
  * :any:`texture-atlas-section`     — Two dimensional texture atlas
  * :any:`depth-texture-section`     — Depth texture
  * :any:`texture-cube-section`      — Texture cube

* :any:`section-variables`

  * :any:`section-variable`  — Generic variable methods
  * :any:`section-uniform`   — Uniform variable
  * :any:`section-attribute` — Attribute variable
  * :any:`section-uniforms`  — Group of uniforms stored in a texture

* :any:`section-framebuffers`

  * :any:`section-render-buffer`  — Generic buffer methods
  * :any:`section-color-buffer`   — Color buffer pbject
  * :any:`section-depth-buffer`   — Depth buffer object
  * :any:`section-stencil-buffer` — Stencil buffer object
  * :any:`section-framebuffer`    — Framebuffer object

* :any:`section-snippet` — Shader injectable code

.. ----------------------------------------------------------------------------
.. toctree::
   :hidden:

   gloo-globject
   gloo-gpudata
   gloo-shader
   gloo-buffer
   gloo-texture
   gloo-variable
   gloo-framebuffer
   gloo-snippet
