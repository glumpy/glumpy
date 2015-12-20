===========================
The OpenGL Shading Language
===========================

The recent trend in graphics hardware has been to replace fixed functionality
with programmability in areas that have grown exceedingly complex (e.g., vertex
processing and fragment processing). The OpenGL Shading Language has been
designed to allow application programmers to express the processing that occurs
at those programmable points of the OpenGL pipeline. Independently compilable
units that are written in this language are called shaders. A program is a set
of shaders that are compiled and linked together.

The OpenGL Shading Language is based on ANSI C and many of the features have
been retained except when they conflict with performance or ease of
implementation. C has been extended with vector and matrix types (with hardware
based qualifiers) to make it more concise for the typical operations carried
out in 3D graphics. Some mechanisms from C++ have also been borrowed, such as
overloading functions based on argument types, and ability to declare variables
where they are first needed instead of at the beginning of blocks.

* OpenGL ES 1.x

  * `OpenGL ES 1.0 <http://www.khronos.org/registry/gles/specs/1.0/opengles_spec_1_0.pdf>`_ (July 21, 2004)
  * `OpenGL ES 1.1 <https://www.khronos.org/registry/gles/specs/1.1/es_full_spec_1.1.12.pdf>`_ (April 24, 2008)

* OpenGL ES 2.x

  * `OpenGL ES 2.0 <https://www.khronos.org/registry/gles/specs/2.0/es_full_spec_2.0.25.pdf>`_ (November 2, 2010)

* OpenGL ES 3.x

  * `OpenGL ES 3.0 <https://www.khronos.org/registry/gles/specs/3.0/es_spec_3.0.4.pdf>`_  (August 27, 2014)
  * `OpenGL ES 3.1 <https://www.khronos.org/registry/gles/specs/3.1/es_spec_3.1.pdf>`_ (April 29, 2015)
  * `OpenGL ES 3.2 <https://www.khronos.org/registry/gles/specs/3.2/es_spec_3.2.pdf>`_ (August 10, 2015)
