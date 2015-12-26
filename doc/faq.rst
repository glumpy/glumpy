.. _pyqtgraph: http://www.pyqtgraph.org
.. _visvis:    https://github.com/almarklein/visvis
.. _galry:     https://github.com/rossant/galry
.. _glumpy:    https://glumpy.github.io
.. _numpy:     http://www.numpy.org
.. _scipy:     http://www.scipy.org 
.. _vispy:     http://vispy.org
.. _Vispy:     http://vispy.org

==========================
Frequently Asked Questions
==========================

**What is the relation between vispy and glumpy ?**

   Vispy_ has been created by Luke Campagnola (pyqtgraph_) , Almar Klein
   (visvis_), Cyrille Rossant (galry_) and myself (Nicolas P. Rougier). During
   this development, I was still using glumpy to experiment some ideas in order
   to later port them into vispy. However, at some point, it was easier for me
   to concentrate only on glumpy and to backport some vispy ideas.

   Glumpy is today more low-level than vispy. Vispy is for the general user
   while glumpy is for the hacker. You can think of glumpy_/vispy_ pretty much
   the same as for numpy_/scipy_ (but vispy does not depend on glumpy).

**Should I use glumpy or vispy?**

   It depends. If you feel comfortable with OpenGL and shaders, you might
   probably benefit from glumpy architecture. However, if you're a scientist
   only interested in having fast and scalable visualization, then you should aim
   at vispy.

**Is glumpy compatible with the Jupyter notebook?**

   Not yet. There are still a number of problems to be solved before something
   happens in that direction.

**Why don't you use this or that feature of OpenGL x.y ?**

   Glumpy tries to stick to OpenGL ES 2.0 in order to maximize the number of
   compatible graphic cards. Some features of glumpy could be easily rewritten
   using latest OpenGL features but this would require extra-effort to write
   two versions of the same feature: one for old cards and one for new cards.

   .. image:: _static/gl-history.png

   Furthermore, giving the slow latency in OpenGL releases, it's hard to stay
   in touch with latest features.
