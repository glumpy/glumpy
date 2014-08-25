<img src="https://raw.githubusercontent.com/rougier/glumpy/master/doc/_static/glumpy.png">

**Glumpy** is a python library for scientific visualization that is both fast,
responsive, and scalable. **Glumpy** offers a natural interface between numpy
and modern OpenGL.


## Dependencies

glumpy is made on top of PyOpenGL (http://pyopengl.sourceforge.net/) and since
glumpy is dedicated to numpy visualization, you obviously need numpy
(http://numpy.scipy.org/). Some demos require Pillow
(https://pypi.python.org/pypi/Pillow) for loading images and ffmpeg
(https://www.ffmpeg.org) for writing/reading movies.


## Example usage

    from glumpy import app

    window = app.Window(512,512)

    @window.event
    def on_draw(dt):
        window.clear()

    app.run()
