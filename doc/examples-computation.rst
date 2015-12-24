.. _game-of-life.py: https://github.com/glumpy/glumpy/blob/master/examples/game-of-life.py
.. _grayscott.py:    https://github.com/glumpy/glumpy/blob/master/examples/grayscott.py
.. _smoke.py:        https://github.com/glumpy/glumpy/blob/master/examples/smoke/smoke.py
.. _GPGPU:           http://gpgpu.org

.. ----------------------------------------------------------------------------
.. _section-examples-computation:

===========
Computation
===========

Glumpy can also be used to perform general General-Purpose Computation on
Graphics Hardware (GPGPU_) without using Cuda or OpenGL. However, things can
become quite complex when you have to deal with several buffers.


* game-of-life.py_
    This examples show a the game of life computed directly on the GPU an is
    very fast.  The example takes care of putting a slider gun in the bottom
    left corner such as to ensure to always have some computation.

* grayscott.py_
    Grayscott reaction-diffusion systems gives really nice different outputs
    depending on the parameters. Make sure to test them all! Inspired from
    `Joakim Linde <http://www.joakimlinde.se/java/ReactionDiffusion/>`_ work.

* smoke.py_
    This is smoke simulation ported from the very nice work of `Philip Rideout
    <http://prideout.net/blog/?p=58>`_ (The Little Grasshoper).
