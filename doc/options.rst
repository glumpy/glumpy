====================
Command line options
====================

Any glumpy program can be started with some options that can override pretty
much any settings. Among the most interesting options, the ``--record`` allows
to record a movie in mp4 format and the ``--fps`` allows to set the framerate
(default is 60 frames per second).


Application
===========

``--backend, -b``
  Backend to use, one of `glfw`, `sdl2`, `pyside`, `pyglet`, `sdl`, `osxglut`.
  Default is `glfw`.

``--interactive, -i``:
  Interactive mode

  .. warning::
  
     Option ``-i`` must come after program name, for example ``python
     gloo-quad.py -i``

``--framerate, -f``:
  Framerate (in frames per second), default is 60.

  .. note::
  
     If you want full acceleration (maximum framerate), you can use ``-f 0``.
                      
``--vsync``:
  Vertical synchronization, disabled by default.

``--size SIZE, -s SIZE``:
  Window initial size

``--position POSITION, -p POSITION``:
  Window initial position

  
Output
======
  
``--display-fps``:
  Display framerate in the console

``--debug, -d``:
  Verbose debug mode
  
``--record``:
  Record a movie (default is "movie.mp4")
  
  
Open GL
=======

``--gl-api API``:
  OpenGL API to use, one of `GL` or `ES`, default is `GL`

``--gl-version VERSION``:
  GL version, default is 2.1

``--gl-profile PROFILE``:
  GL context profile (only relevant for GL > 3.0), one of `none`, `core`,
  `compatibility`.

``--srgb``:
  sRGB mode (gamma correction), disabled by default.

``--depth-size SIZE``:
  Depth buffer size in bits, default is 16.

``--stentil-size SIZE``:
  Stencilbuffer size in bits, default is 0 (no stencil).

``--single-buffer``:
  Single buffer mode. Not recommended, default is double buffer mode.

``--stereo``:
  Stereo mode, disabled by default.

