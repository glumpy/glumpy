======================
Command line arguments
======================

Any glumpy program can be fed with default command line arguments that can
override any settings.

``--backend``, ``-b``:
  Backend to use, one of `glfw`, `sdl2`, `pyside`, `pyglet`, `sdl`, `osxglut`.
  Default is `glfw`.

``--framerate``, ``-f``:
  Framerate (in frames per second), default is 60. If you want full
  acceleration (maximum framerate), you can use 0.

``--display-fps``:
  Display the actual framerate (estimation) every second.

``--api``:
  OpenGL API to use, one of `GL` or `ES`, default is `GL`

``--version``:
  GL version, default is 2.1

``--profile``:
  GL context profile (only relevant for GL > 3.0), one of `none`, `core`, `compatibility`.

``--vsync``:
  Vertical synchronization, disabled by default.

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
