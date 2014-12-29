<img src="https://raw.githubusercontent.com/rougier/glumpy/master/doc/_static/glumpy-teaser.png">

**Glumpy** is a python library for scientific visualization that is both fast,
scalable and beautiful. **Glumpy** offers a natural interface between numpy
and modern OpenGL.

## Installation

```
git clone https://github.com/glumpy/glumpy.git
cd glumpy
python setup.py install
cd examples
./app-simple.py
```

## Dependencies

### Mandatory

* PyOpenGL: http://pyopengl.sourceforge.net/
* Numpy: http://numpy.scipy.org/


### Optional

* Cython: http://cython.org
* PIL or Pillow: https://pypi.python.org/pypi/Pillow
* ffmpeg: https://www.ffmpeg.org
* freetype: http://www.freetype.org
* triangle: http://dzhelil.info/triangle/index.html


### Embedded

glumpy makes use of a number of great external tools that are directly embedded
within the repository. Here is a list:

* [moviepy](https://github.com/Zulko/moviepy) by Zulko
* [pypng](<https://github.com/drj11/pypng>) by David Jones
* ìnputhook management from [IPython](https://github.com/ipython/ipython)
* [six](https://pypi.python.org/pypi/six/) utilities for writing code that runs
  on Python 2 and 3 by Benjamin Peterson


## Example usage

    from glumpy import app

    window = app.Window(512,512)

    @window.event
    def on_draw(dt):
        window.clear()

    app.run()
