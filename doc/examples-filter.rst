.. _filter-pixelate.py: https://github.com/glumpy/glumpy/blob/master/examples/filter-pixelate.py
.. _filter-blur.py:     https://github.com/glumpy/glumpy/blob/master/examples/filter-blur.py
.. _filter-compose.py:  https://github.com/glumpy/glumpy/blob/master/examples/filter-compose.py

.. ----------------------------------------------------------------------------
.. _section-examples-filter:

=======
Filters
=======

Post-processing filters are easily implemented using the Filter object. You
draw tour scene normally but draw calls are surrounded by a ```with
Filter(shader)`` where the shader transform the output.

* filter-pixelate.py_
    Pixelating filter with pixelation level controlled by mouse scroll.

* filter-blur.py_
    Simple 2D Gaussian blur using two 1D kernels.

* filter-compose.py_
    This example show how to compose filters together.

.. note::

   You will find several other very nice filters in the `GPUImage
   <https://github.com/BradLarson/GPUImage>`_ repository.
