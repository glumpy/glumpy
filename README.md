.. image:: https://raw.githubusercontent.com/rougier/glumpy/master/doc/_static/glumpy.png

**Glumpy** is a python library for scientific visualization that is both fast,
responsive, and scalable. **Glumpy** offers a natural interface between numpy
and modern OpenGL.


## Example usage

::

    from glumpy import app

    window = app.Window(512,512)

    @window.event
    def on_draw(dt):
        window.clear()

    app.run()
