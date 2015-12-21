======================
Command line arguments
======================

Any glumpy program can be fed with default command line arguments that can
override pretty much any settings.


Application
===========

These settings relate to the initial window creation and interactivity.

--backend, -b         Backend to use, one of `glfw`, `sdl2`, `pyside`, `pyglet`, `sdl`, `osxglut`.
                      Default is `glfw`.

--interactive, -i     Interactive mode

--framerate, -f       Framerate (in frames per second), default is 60.

                      If you want full acceleration (maximum framerate), you can use 0.
                      
--vsync               Vertical synchronization, disabled by default.

--size SIZE, -s SIZE  Window initial size

--position POSITION, -p POSITION
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

``--gl-api``:
  OpenGL API to use, one of `GL` or `ES`, default is `GL`

``--gl-version``:
  GL version, default is 2.1

``--gl-profile``:
  GL context profile (only relevant for GL > 3.0), one of `none`, `core`,
  `compatibility`.

``--srgb``:
  sRGB mode (gamma correction), disabled by default.

``--depth-size``:
  Depth buffer size in bits, default is 16.

``--stentil-size``:
  Stencilbuffer size in bits, default is 0 (no stencil).

``--single-buffer``:
  Single buffer mode. Not recommended, default is double buffer mode.

``--stereo``:
  Stereo mode, disabled by default.

