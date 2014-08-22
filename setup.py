#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Copyright (C) 2009,2010,2011  Nicolas P. Rougier
#
# Distributed under the terms of the BSD License. The full license is in
# the file COPYING, distributed as part of this software.
#-----------------------------------------------------------------------------
import os
# import numpy
# from Cython.Distutils import build_ext
from distutils.core import setup, Extension

if __name__ == "__main__":

    if os.path.exists('MANIFEST'):
        os.remove('MANIFEST')

    setup(name="glumpy",
          version="2.0",
          description="",
          long_description = "",
          maintainer= "Nicolas P. Rougier",
          maintainer_email="Nicolas.Rougier@inria.fr",
          license = "BSD License",
          packages=['glumpy',
                    'glumpy.app',
                    'glumpy.gloo',

                    'glumpy.data',
                    'glumpy.data.arrays',
                    'glumpy.data.fonts',
                    'glumpy.data.images',
                    'glumpy.data.objects',

                    'glumpy.shaders',
                    'glumpy.shaders.math',
                    'glumpy.shaders.paths',
                    'glumpy.shaders.arrows',
                    'glumpy.shaders.markers',
                    'glumpy.shaders.filters',
                    'glumpy.shaders.antialias',
                    'glumpy.shaders.transforms',
                    'glumpy.shaders.collections',

                    'glumpy.filters',
                    'glumpy.geometry',
                    'glumpy.graphics',
                    'glumpy.transforms' ],
          package_data={
              'glumpy.data.arrays':         ['*.npy'],
              'glumpy.data.fonts':          ['*.ttf', '*.txt'],
              'glumpy.data.images':         ['*.png', '*.jpg'],
              'glumpy.data.objects':        ['*.obj', "*.txt"],
              'glumpy.shaders':             ['*.vert','*.frag', "*.geom", "*.glsl"],
              'glumpy.shaders.math':        ['*.vert','*.frag', "*.geom", "*.glsl"],
              'glumpy.shaders.paths':       ['*.vert','*.frag', "*.geom", "*.glsl"],
              'glumpy.shaders.arrows':      ['*.vert','*.frag', "*.geom", "*.glsl"],
              'glumpy.shaders.markers':     ['*.vert','*.frag', "*.geom", "*.glsl"],
              'glumpy.shaders.filters':     ['*.vert','*.frag', "*.geom", "*.glsl"],
              'glumpy.shaders.antialias':   ['*.vert','*.frag', "*.geom", "*.glsl"],
              'glumpy.shaders.transforms':  ['*.vert','*.frag', "*.geom", "*.glsl"],
              'glumpy.shaders.collections': ['*.vert','*.frag', "*.geom", "*.glsl"]
          },

#          cmdclass={'build_ext': build_ext},
#          ext_modules=[Extension("glumpy.ext.sdf",
#                                 sources=["glumpy/ext/sdf/_sdf.pyx",
#                                          "glumpy/ext/sdf/sdf.c"],
#                                 include_dirs=[numpy.get_include()])],

)
