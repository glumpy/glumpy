#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Copyright (C) 2009,2010,2011  Nicolas P. Rougier
#
# Distributed under the terms of the BSD License. The full license is in
# the file COPYING, distributed as part of this software.
#-----------------------------------------------------------------------------
import os
import numpy
from distutils.core import setup, Extension
from Cython.Distutils import build_ext


if __name__ == "__main__":
    setup(name="glumpy",
          version="alpha",
          description="",
          long_description = "",
          maintainer= "Nicolas P. Rougier",
          maintainer_email="Nicolas.Rougier@inria.fr",
          license = "BSD License",
          packages=['glumpy',
                    'glumpy.app',
                    'glumpy.gloo',
                    'glumpy.data',
                    'glumpy.shaders',
                    'glumpy.filters',
                    'glumpy.geometry',
                    'glumpy.graphics',
                    'glumpy.transforms' ],
          cmdclass={'build_ext': build_ext},
          ext_modules=[Extension("glumpy.ext.sdf",
                                 sources=["glumpy/ext/sdf/_sdf.pyx",
                                          "glumpy/ext/sdf/sdf.c"],
                                 include_dirs=[numpy.get_include()])],

)
