=======
Filters
=======

Post-processing filters are easily implemented using the Filter object. You
draw tour scene normally but the draw calls are surrounded by a ```with
Filter(shader)`` where the shader transform the otuput.

* `filter-pixelate.py <https://github.com/glumpy/glumpy/blob/master/examples/filter-sepia.py>`_

  Pixelating filter with pixelation level controlled by mouse scroll.


* `filter-blur.py <https://github.com/glumpy/glumpy/blob/master/examples/filter-blur.py>`_

  Simple 2D Gaussian blur using two 1D kernels.


* `filter-composition.py <https://github.com/glumpy/glumpy/blob/master/examples/filter-composition.py>`_

  This example show how to compose filters together.
