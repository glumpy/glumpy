============
Installation
============


Packages requirements
=====================

The only mandatory requirements for glumpy is the `numpy <http://numpy.org>`_
and the `pyopengl <http://pyopengl.sourceforge.net>`_ packages. The most
straightforward way to install them is:

.. code-block:: bash

   $ pip install numpy
   $ pip install pyopengl

If you have alread installed them, make sure to upgrade to the lastest version:

.. code-block:: bash

   $ pip install --upgrade numpy
   $ pip install --upgrade pyopengl


Backends requirements
=====================

Glumpy requires at least one toolkit for opening a window and creates an OpenGL
context. This can be done using one of the standard C/C++ toolkits (Qt, GLFW,
glut, pygame, SDL2, Wx, GTK2 or GTK3) and requires the corresponding python
bindings or a pure python toolkit such as pyglet.

.. warning::

   You only need to have one of these packages, no need to install them all !

===================== === ==== ====== ==== ==== ===
**Modern Backends**   Qt  GLFW Pyglet SDL2 GTK3 Wx3
--------------------- --- ---- ------ ---- ---- ---
Multiple windows       ✓   ✓     ✓     ✓    ✓    ✓
--------------------- --- ---- ------ ---- ---- ---
Non-decorated windows  ✓   ✓     ✓     ✓    ✓    ✓
--------------------- --- ---- ------ ---- ---- ---
Resize windows         ✓   ✓     ✓     ✓    ✓    ✓
--------------------- --- ---- ------ ---- ---- ---
Move windows           ✓   ✓     ✓     ✓    ✓    ✓
--------------------- --- ---- ------ ---- ---- ---
Set GL API             ✓   ✓    —      ✓    ✓    ✓
--------------------- --- ---- ------ ---- ---- ---
Set GL Profile         ✓   ✓    —      ✓    ✓    ✓
--------------------- --- ---- ------ ---- ---- ---
Share GL Context       ✓   ✓     ✓     ✓    ✓    ✓
--------------------- --- ---- ------ ---- ---- ---
Fullscreen             ✓   ✓     ✓     ✓    ✓    ✓
--------------------- --- ---- ------ ---- ---- ---
Unicode handling       ✓   ✓     ✓     ✓    ✓    ✓
===================== === ==== ====== ==== ==== ===

|

======================== === ==== ======== ====== =======
**Old school backends**  Wx2 Glut Freeglut Pygame GTK 2.x
------------------------ --- ---- -------- ------ -------
Multiple windows          ✓   —      —       —      ✓
------------------------ --- ---- -------- ------ -------
Non-decorated windows     ✓   ✓      ✓       ✓      ✓
------------------------ --- ---- -------- ------ -------
Resize windows            ✓   ✓      ✓       —      ✓
------------------------ --- ---- -------- ------ -------
Move windows              ✓   ✓      ✓       —      ✓
------------------------ --- ---- -------- ------ -------
Set GL API                —   —      —       —      —
------------------------ --- ---- -------- ------ -------
Set GL Profile            —   —      —       —      —
------------------------ --- ---- -------- ------ -------
Share GL Context          —   —      —       —      ✓
------------------------ --- ---- -------- ------ -------
Fullscreen                ✓  ✓       ✓       ✓      ✓
------------------------ --- ---- -------- ------ -------
Unicode handling          ✓   —      —       ✓      ✓
------------------------ --- ---- -------- ------ -------
Scroll event              ✓   —      ✓       —      ✓
======================== === ==== ======== ====== =======


Qt
--

`Qt <http://qt-project.org>`_ is a cross-platform application and UI framework
for developers using C++ or QML, a CSS & JavaScript like language. Qt Creator
is the supporting Qt IDE. There are (at least) two sets of availble python
bindings. `PyQT <http://pyqt.sourceforge.net>`_ supports Python v2 and v3 and
Qt v4 and Qt v5 and is available under the GPL and commercial licenses. `PySide
<http://qt-project.org/wiki/PySide>`_ provides LGPL-licensed Python bindings
for Qt. PySide Qt bindings allow both free open source and proprietary software
development and ultimately aim to support Qt platforms.

GLFW
----

`GLFW <http://www.glfw.org>`_ is an Open Source, multi-platform library for
creating windows with OpenGL contexts and managing input and events. It is easy
to integrate into existing applications and does not lay claim to the main
loop. There is no need to install bindings because glumpy comes with the glfw
bindings (cloned from the `pyglfw <https://github.com/rougier/pyglfw>`_ project).

GLUT
----

`GLUT <http://www.opengl.org/resources/libraries/glut/>`_ is the OpenGL Utility
Toolkit, a window system independent toolkit for writing OpenGL programs. It
implements a simple windowing application programming interface (API) for
OpenGL. `PyOpenGL <http://pyopengl.sourceforge.net>`_ is the most common
cross platform Python binding to OpenGL and related APIs. The binding is
created using the standard ctypes library and gives access to GLUT.

Pyglet
------

`Pyglet <http://www.pyglet.org>`_ is a cross-platform windowing and multimedia
library for Python and provides an object-oriented programming interface for
developing games and other visually-rich applications for Windows, Mac OS X
and Linux.


SDL2 (a.k.a. PyGame2)
---------------------

`PySDL2 <http://www.pygame.org>`_ is a wrapper around the SDL2 library and as
such similar to the discontinued PySDL project. In contrast to PySDL, it has no
licensing restrictions, nor does it rely on C code, but uses ctypes instead.


GTK 2.x (not yet done)
----------------------

GTK 3.x (not yet done)
----------------------

WX 2.x (not yet done)
---------------------

WX 3.x (not yet done)
---------------------

PyGame (a.k.a. SDL)
-------------------

`Pygame <http://www.pygame.org>`_ is a set of Python modules designed for
writing games. Pygame adds functionality on top of the excellent SDL
library. This allows you to create fully featured games and multimedia programs
in the python language. Pygame is highly portable and runs on nearly every
platform and operating system.



Hardware requirements
=====================

Glumpy makes heavy use of the graphic cards installed on your system. More
precisely, glumpy makes heavy use of the Graphical Processing Unit (GPU) through
shaders. Glumpy thus requires a fairly recent video card (~ less than 12 years
old) as well as an up-to-date video driver such that glumpy can access the
programmable pipeline (as opposed to the fixed pipeline).


Linux and OSX
-------------

On Linux and OSX platform, you can type:

.. code-block:: bash

   $ glxinfo

The results of the above command and is long list of information related to
your video driver. The most important information for the time being is whether
you have direct access to your video card and what is the GL version and the
shading language version::

   ...
   direct rendering: Yes
   ...
   OpenGL vendor string: NVIDIA Corporation
   OpenGL renderer string: NVIDIA GeForce GT 650M OpenGL Engine
   OpenGL version string: 2.1 NVIDIA-8.24.9 310.40.25f01
   OpenGL shading language version string: 1.20
   ...


The OpenGL version must be at least 2.1 and the shading language version must
be at least 1.1. If this is not the case, you need to install more recent
versions. Have a look a your system documentation or browse online for howtos.


Windows
-------

To be written.



Installation
============

Once requirements are met, you can proceed with glumpy installation:

.. code-block:: bash

   pip install glumpy

or upgrade any existing installation:

.. code-block:: bash

   pip install --upgrade glumpy


Testing installation
--------------------

It is strongly advised to run the glumpy test suite right after installation to
check if everything is ok. To do this, just type:

.. code-block:: pycon

   >>> import glumpy
   >>> glumpy.test()
   ...
