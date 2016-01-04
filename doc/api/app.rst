=======================
Application layer (app)
=======================

The ``glumpy.app`` module gathers all classes and methods necessary to open a
window, create a GL context and handle events.

* :any:`section-windows`       — Window related objects

  * :any:`section-window`      — Main window class

    * :any:`section-event`       — Event management
    * :any:`section-key`         — Keyboard events
    * :any:`section-mouse`       — Mouse events
      
  * :any:`section-backends`    — Window backends

    * :any:`section-backend-freeglut` — Freeglut
    * :any:`section-backend-osxglut`  — OSX Glut
    * :any:`section-backend-glfw`     — GLFW
    * :any:`section-backend-pyglet`   — Pyglet
    * :any:`section-backend-sdl`      — PyGame (SDL 1.x)
    * :any:`section-backend-sdl2`     — SDL 2.0
    * :any:`section-backend-pyside`   — PySide (Qt 4.x)
    * :any:`section-backend-template` — Backend template

* :any:`section-viewport`      — Viewport area
* :any:`section-configuration` — OpenGL context configuration
* :any:`section-clock`         — Time management
* :any:`section-console`       — Failsafe console
* :any:`section-parser`        — Command line parser & default settings


.. toctree::
   :hidden:

   app-window
   app-backends
   app-viewport
   app-configuration
   app-clock
   app-console
   app-parser
