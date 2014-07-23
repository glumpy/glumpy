from distutils.core import setup, Extension
import numpy
from Cython.Distutils import build_ext

setup(
    cmdclass={'build_ext': build_ext},
    ext_modules=[Extension("sdf",
                 sources=["_sdf.pyx", "sdf.c"],
                 include_dirs=[numpy.get_include()])],
)
