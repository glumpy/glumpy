.. _app-backend.py:      https://github.com/glumpy/glumpy/blob/master/examples/app-backend.py
.. _app-config.py:       https://github.com/glumpy/glumpy/blob/master/examples/app-config.py
.. _app-event-loop.py:   https://github.com/glumpy/glumpy/blob/master/examples/app-event-loop.py
.. _app-events.py:       https://github.com/glumpy/glumpy/blob/master/examples/app-events.py
.. _app-interactive.py:  https://github.com/glumpy/glumpy/blob/master/examples/app-interactive.py
.. _app-screenshot.py:   https://github.com/glumpy/glumpy/blob/master/examples/app-screenshot.py
.. _app-simple.py:       https://github.com/glumpy/glumpy/blob/master/examples/app-simple.py
.. _app-timed.py:        https://github.com/glumpy/glumpy/blob/master/examples/app-timed.py
.. _app-two-windows.py:  https://github.com/glumpy/glumpy/blob/master/examples/app-two-windows.py
.. _app-two-programs.py: https://github.com/glumpy/glumpy/blob/master/examples/app-two-programs.py

.. ----------------------------------------------------------------------------
.. _section-examples-app:
   
=================
Application layer
=================

The ``glumpy.app`` layer is responsible for opening a window and handling
events (mouse, keyboard and user event). It also provides convenient interfaces
to parse command line options and configure the OpenGL context.


* app-backend.py_
    This example shows how to change the backend programmatically.

    .. warning::

       Note that if the backend is set, the ``--backend`` command line option has not effect.
    
* app-config.py_
    This example shows how to choose and use a specific GL configuration (GL
    version & profile, depth buffer size, stencil, ...).
  
* app-event-loop.py_
    This example shows how to run manually the event loop.
    It might come handy if you want to integrate a glumpy program into another application.

* app-events.py_
    This example exhibits all available events and display them when triggered.

    .. note::

       Note that the idle event is commented out because it generates far too many messages.

* app-interactive.py_
    This example runs in interactive mode where python console is reactive.

* app-screenshot.py_
    This examples takes a single screenshot and immeditaley exit.

    .. note::

       You can also take a screenshot anytime using the ``F10`` key. The
       screenshot will be named after the example filename.

* app-simple.py_
    This is the most simple glumpy example that display a black window and wait
    for the user to exit the application

    .. note::

       You can exit any glumpy program by closing the window or pressing the
       ``ESC`` key. If you want to disable the ``ESC`` behavior, you'll have to
       connect to the key press event and override behavior.

* app-timed.py_
    This example creates a window and closes it after 5 seconds.

* app-two-windows.py_
    This example opens two windows, one should be black, the other white.

* app-two-programs.py_
    This example displays two points (square), one blue, one red, using two
    shader programs. This example also serves as a test for checking glumpy is
    running properly.
