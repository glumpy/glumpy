<img src="https://raw.githubusercontent.com/rougier/glumpy/master/doc/_static/glumpy-teaser.png">

**Glumpy** is a python library for scientific visualization that is both fast,
responsive, and scalable. **Glumpy** offers a natural interface between numpy
and modern OpenGL.


## Dependencies

### Mandatory

* PyOpenGL: http://pyopengl.sourceforge.net/
* Numpy: http://numpy.scipy.org/

### Optional

* PIL or Pillow: https://pypi.python.org/pypi/Pillow
* ffmpeg: https://www.ffmpeg.org
* freetype: http://www.freetype.org


## Example usage

    from glumpy import app

    window = app.Window(512,512)

    @window.event
    def on_draw(dt):
        window.clear()

    app.run()
