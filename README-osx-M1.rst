Installing on M1 Macs
=====================

Installing via ``pip`` on an Apple Silicon/M1 Mac may fail due to an incompatibility with the pre-generated Cython code for the  ``triangle`` dependency. As a workaround, this package and glumpy can be downloaded from GitHub and installed manually, like this:

::
   
   # dependencies
   pip install numpy Cython PyOpenGL
   
   # manually install triangle
   git clone --recurse-submodules https://github.com/drufat/triangle
   cd triangle
   python setup.py install
   
   # manually install glumpy
   cd ..
   git clone https://github.com/glumpy/glumpy
   cd glumpy
   python setup.py install

At this point glumpy should be installed, but if you try to run one of the examples (e.g. ``python examples/hello-world.py``) you may receive ``RuntimeError: Freetype library not found``. This occurs if you have installed freetype via Homebrew, which does not add the library directory to the system path. To fix this add the path manually:

::
   
   # either
   export DYLD_LIBRARY_PATH=$(brew --prefix freetype)/lib:$DYLD_LIBRARY_PATH
   # or
   export DYLD_LIBRARY_PATH=$(freetype-config --prefix)/lib:$DYLD_LIBRARY_PATH
   
   python examples/hello-world.py # works now!
