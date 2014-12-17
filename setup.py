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
from Cython.Distutils import build_ext
# from distutils.core import setup, Extension
from setuptools import setup, Extension

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
                    'glumpy.ext',
                    'glumpy.ext.sdf',
                    'glumpy.ext.freetype',
                    'glumpy.ext.freetype.ft_enums',
                    'glumpy.app',
                    'glumpy.app.window',
                    'glumpy.app.window.backends',
                    'glumpy.gloo',

                    'glumpy.data',
                    'glumpy.data.arrays',
                    'glumpy.data.fonts',
                    'glumpy.data.images',
                    'glumpy.data.objects',

                    'glumpy.library',
                    'glumpy.library.math',
                    'glumpy.library.paths',
                    'glumpy.library.arrows',
                    'glumpy.library.markers',
                    'glumpy.library.filters',
                    'glumpy.library.antialias',
                    'glumpy.library.transforms',
                    'glumpy.library.collections',

                    'glumpy.filters',
                    'glumpy.geometry',
                    'glumpy.graphics',
                    'glumpy.transforms',
                    'glumpy.graphics.text',
                    'glumpy.graphics.collection'],

          package_data={
              'glumpy.data.arrays':         ['*.npy'],
              'glumpy.data.fonts':          ['*.ttf', '*.txt'],
              'glumpy.data.images':         ['*.png', '*.jpg'],
              'glumpy.data.objects':        ['*.obj', "*.txt"],
              'glumpy.library':             ['*.vert','*.frag', "*.geom", "*.glsl"],
              'glumpy.library.math':        ['*.vert','*.frag', "*.geom", "*.glsl"],
              'glumpy.library.paths':       ['*.vert','*.frag', "*.geom", "*.glsl"],
              'glumpy.library.arrows':      ['*.vert','*.frag', "*.geom", "*.glsl"],
              'glumpy.library.markers':     ['*.vert','*.frag', "*.geom", "*.glsl"],
              'glumpy.library.filters':     ['*.vert','*.frag', "*.geom", "*.glsl"],
              'glumpy.library.antialias':   ['*.vert','*.frag', "*.geom", "*.glsl"],
              'glumpy.library.transforms':  ['*.vert','*.frag', "*.geom", "*.glsl"],
              'glumpy.library.collections': ['*.vert','*.frag', "*.geom", "*.glsl"]
          },

          cmdclass={'build_ext': build_ext},
          ext_modules=[Extension("glumpy.ext.sdf",
                                 sources=["glumpy/ext/sdf/_sdf.pyx",
                                          "glumpy/ext/sdf/sdf.c"],
                                 include_dirs=[numpy.get_include()])],
)
