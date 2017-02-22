============
Installation
============


The most straightforward way to install glumpy is to use pip:

.. code-block:: bash

   pip install glumpy

or upgrade any existing installation:

.. code-block:: bash

   pip install --upgrade glumpy

   
Packages requirements
=====================

Mandatory requirements for glumpy are:

 * numpy:    http://numpy.org
 * pyopengl: http://pyopengl.sourceforge.net
 * cython:   http://cython.org
 * triangle: http://dzhelil.info/triangle/

The most easy way to install these dependencies is:
   
.. code-block:: bash

   $ pip install numpy
   $ pip install cython
   $ pip install pyopengl
   $ pip install triangle

If you have alread installed them, make sure to upgrade to the latest version:

.. code-block:: bash

   $ pip install --upgrade numpy
   $ pip install --upgrade pyopengl
   $ pip install --upgrade cython
   $ pip install --upgrade triangle


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



Hardware requirements
=====================

Glumpy makes heavy use of the graphic cards installed on your system. More
precisely, glumpy makes heavy use of the Graphical Processing Unit (GPU)
through shaders. Glumpy thus requires a fairly recent video card (~ less than
12 years old) as well as an up-to-date video driver such that glumpy can access
the programmable pipeline (as opposed to the fixed pipeline).

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

Step-by-step install for x64 bit Windows 7,8, and 10.
=========================================================

1. Install Python:
  - Download Python 3.x from here https://www.python.org/downloads/
  - Run the executable, install to a short path (e.g. "C:\\python3")
  - Add the Python executable folder to the system path (Usually done during install)
  - **reboot for system changes to take effect**
  After reboot, it's a good idea to type "python" at the command line to make sure the system can find it. You should get the usual ">>>" python CLI console. If not, it's 99% likely the path to python needs added manually.

2. Install dependencies (**From elevated command prompt**)::

    C:\Windows\system32> pip install numpy
    C:\Windows\system32> pip install cython
    C:\Windows\system32> pip install pyopengl
    C:\Windows\system32> pip install triangle

3. Install glumpy (**From elevated command prompt**)::

    C:\Windows\system32> pip install glumpy

4. Install freetype:
  - Download a precompiled x64 version from here. https://github.com/ubawurinna/freetype-windows-binaries	
  - Extract the zip somewhere
  - Copy either of the freetype.dlls in the win64 folder to your python3 folder.
  - Rename the freetype dll file to just "freetype.dll"
  The README explains the file differences; files with MT in the name are preferred.

5. Install GLFW:
  - Download the x64 bit version from here. http://www.glfw.org/download.html
  - Extract the zip somewhere
  - Copy one of the glfw.dll files from one of the "lib-xxxxx" folders to your python3 folder.
  The preferred file is probably from "lib-mingw-w64," you do not need to rename it.
