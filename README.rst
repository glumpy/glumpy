Description
===========

glumpy is a python library for the rapid vizualization of numpy arrays, (mainly
two dimensional) that has been designed with efficiency in mind. If you want to
draw nice figures for inclusion in a scientific article, you'd better use
matplotlib. If you want to have a sense of what's going on in your simulation
while it is running, then glumpy can help you.


Dependencies
============
glumpy is made on top of PyOpenGL (http://pyopengl.sourceforge.net/) and since
glumpy is dedicated to numpy visualization, you obviously need numpy
(http://numpy.scipy.org/).

Some demos require Pillow (https://pypi.python.org/pypi/Pillow) for loading
images and ffmpeg (https://www.ffmpeg.org) for writing/reading movies.


Example usage
=============

::

    from glumpy import app

    window = app.Window(512,512)

    @window.event
    def on_draw(dt):
        window.clear()

    app.run()
