Shaders
=======

A Shader is a user-defined program designed to be executed at a given stage of
the rendering pipeline.

Shaders are pieces of program (using a C-like language) that are build onto the
GPU and executed during the rendering pipeline. Depending on the nature of the
shaders (there are many types depending on the version of OpenGL you're using),
they will act at different stage of the rendering pipeline. Glumpy stick to the
OpenGL ES version where only **vertex** and **fragment** shaders are available.

.. Note::

   The shader language is called glsl. There are many versions that goes from 1.0
   to 1.5 and subsequents version get the number of OpenGL version. Last version
   is 4.4 (February 2014).


Vertex shader
-------------

Fragment shader
---------------
