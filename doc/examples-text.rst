.. _font-agg.py:         https://github.com/glumpy/glumpy/blob/master/examples/font-agg.py
.. _font-sdf.py:         https://github.com/glumpy/glumpy/blob/master/examples/font-sdf.py
.. _font-atlas.py:       https://github.com/glumpy/glumpy/blob/master/examples/font-atlas.py
.. _font-atlas.py:       https://github.com/glumpy/glumpy/blob/master/examples/font-atlas.py
.. _gloo-console.py:     https://github.com/glumpy/glumpy/blob/master/examples/gloo-console.py
.. _gloo-terminal.py:    https://github.com/glumpy/glumpy/blob/master/examples/gloo-terminal.py
.. _collection-glyph.py: https://github.com/glumpy/glumpy/blob/master/examples/collection-glyph.py

.. ----------------------------------------------------------------------------
.. _section-examples-text:

============
Text & fonts
============

Glumpy uses several techniques for displaying text but the most versatile is
the signed distance field rendering techniques.


* font-agg.py_
    This examples displays the same text at different size with perfect legibility.

* font-sdf.py_
    This examples displays the same text at different size with quasi-perfect legibility.

* font-atlas.py_
    This examples shosw how glyphs are packed into a texture atlas.

* collection-glyph.py_
    This examples displays a text in 3D (use mouse to manipulate)

* gloo-console.py_
    This examples show how to use the on-screen console that should never fails.

    .. note::

       The console is fairly limited and must be used for debugging purposes only.

* gloo-terminal.py_
    This examples show a more complete terminal that is able to scroll and to
    display an extended set of characters (just scroll to see them). It is very
    fast and can be used for quick'n'dirty input/output.

    .. note::

       The terminal uses a dedicated technique to ensure rendering speed. For
       better text output, one must used a glyph collection.

