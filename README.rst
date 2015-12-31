
.. image:: https://raw.githubusercontent.com/rougier/glumpy/master/doc/_static/glumpy-teaser.png

**Glumpy** is a python library for scientific visualization that is both fast,
scalable and beautiful. **Glumpy** offers a natural interface between numpy
and modern OpenGL.

======================= ====================================================
**Source repository**   https://github.com/glumpy/glumpy
**Issue tracker**       https://github.com/glumpy/glumpy/issues
**Website**             http://glumpy.github.io
**Gallery**             http://glumpy.github.io/gallery.html
**Documentation**       http://glumpy.readthedocs.org/en/latest/
**Chatroom**            https://gitter.im/glumpy/chatroom
**Mailing list**        https://groups.google.com/forum/#!forum/glumpy-users
======================= ====================================================

Installation
============

::

  git clone https://github.com/glumpy/glumpy.git
  cd glumpy
  python setup.py install
  cd examples
  ./app-simple.py

Dependencies
============

Python
------

* PyOpenGL: http://pyopengl.sourceforge.net/
* Numpy: http://numpy.scipy.org/
* Cython: http://cython.org
* triangle: http://dzhelil.info/triangle/index.html

System
------

* ffmpeg: https://www.ffmpeg.org
* freetype: http://www.freetype.org

Embedded
--------

glumpy makes use of a number of great external tools that are directly embedded
within the repository. Here is a list:

* `moviepy <https://github.com/Zulko/moviepy>`_ by Zulko
* `pypng <https://github.com/drj11/pypng>`_ by David Jones
* inputhook management from `IPython <https://github.com/ipython/ipython>`_
* `six <https://pypi.python.org/pypi/six/>`_ utilities for writing code that runs
  on Python 2 and 3 by Benjamin Peterson

Example usage
=============

::

    from glumpy import app

    window = app.Window(512,512)

    @window.event
    def on_draw(dt):
        window.clear()

    app.run()

More...
=======

.. image:: https://raw.githubusercontent.com/rougier/glumpy/master/doc/_static/poster.png
