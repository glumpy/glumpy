#-----------------------------------------------------------------------------
# Copyright (C) 2011-2016  Nicolas P. Rougier
#
# Distributed under the terms of the BSD License. The full license is in
# the file COPYING, distributed as part of this software.
#-----------------------------------------------------------------------------
import os
import numpy
from Cython.Distutils import build_ext
from setuptools import setup, Extension

if __name__ == "__main__":

    if os.path.exists('MANIFEST'):
        os.remove('MANIFEST')

    setup(name="glumpy",
          version="1.0.6",
          description="Fast, scalable & beautiful scientific visualisation",
          long_description = """Glumpy is a python library for scientific
                                visualization that is both fast, scalable
                                and beautiful. Glumpy offers an intuitive
                                interface between numpy and modern OpenGL.""",
          url = "http://glumpy.github.io",
          download_url = "https://github.com/glumpy/glumpy/releases",
          keywords = "OpenGL, GLSL, 2D, 3D, Visualisation, Science, Numpy, Graphics, Shaders",
          platform = "Any",
          maintainer= "Nicolas P. Rougier",
          maintainer_email="Nicolas.Rougier@inria.fr",
          install_requires=['numpy', 'triangle', 'cython'],
          classifiers=[
              "Development Status :: 4 - Beta",
              "Operating System :: MacOS :: MacOS X",
              "Operating System :: Microsoft :: Windows",
              "Operating System :: POSIX",
              "Programming Language :: Python :: 2.7",
              "License :: OSI Approved :: BSD License",
              "Intended Audience :: Developers",
              "Intended Audience :: Science/Research",
              "Topic :: Scientific/Engineering :: Visualization",
              "Topic :: Multimedia :: Graphics",
          ],
          license = "BSD License",
          packages=['glumpy',
                    'glumpy.data',
                    'glumpy.ext',
                    'glumpy.ext.sdf',
                    'glumpy.ext.freetype',
                    'glumpy.ext.freetype.ft_enums',
                    'glumpy.app',
                    'glumpy.app.window',
                    'glumpy.app.window.backends',
                    'glumpy.gloo',
                    'glumpy.api',
                    'glumpy.api.matplotlib',

                    'glumpy.library',
                    'glumpy.library.math',
                    'glumpy.library.misc',
                    'glumpy.library.arrows',
                    'glumpy.library.markers',
                    'glumpy.library.colormaps',
                    'glumpy.library.antialias',
                    'glumpy.library.transforms',
                    'glumpy.library.collections',

                    'glumpy.geometry',
                    'glumpy.graphics',
                    'glumpy.graphics.svg',
                    'glumpy.graphics.color',
                    'glumpy.transforms',
                    'glumpy.graphics.text',
                    'glumpy.graphics.collections'],

          package_data={
              'glumpy.ext.sdf':             ['_sdf.pyx', 'sdf.h'],
              'glumpy.data':                ['6x13-italic.npy',
                                             '6x13-regular.npy',
                                             '6x13-bold.npy',
                                             'spatial-filters.npy',
                                             'SourceSansPro-Regular.otf' ],
              'glumpy.library':             ['*.vert','*.frag', "*.geom", "*.glsl"],
              'glumpy.library.math':        ['*.vert','*.frag', "*.geom", "*.glsl"],
              'glumpy.library.misc':        ['*.vert','*.frag', "*.geom", "*.glsl"],
              'glumpy.library.arrows':      ['*.vert','*.frag', "*.geom", "*.glsl"],
              'glumpy.library.markers':     ['*.vert','*.frag', "*.geom", "*.glsl"],
              'glumpy.library.colormaps':   ['*.vert','*.frag', "*.geom", "*.glsl"],
              'glumpy.library.antialias':   ['*.vert','*.frag', "*.geom", "*.glsl"],
              'glumpy.library.transforms':  ['*.vert','*.frag', "*.geom", "*.glsl"],
              'glumpy.library.collections': ['*.vert','*.frag', "*.geom", "*.glsl"]
          },

          cmdclass={'build_ext': build_ext},
          ext_modules=[Extension("glumpy.ext.sdf.sdf",
                                 sources=["glumpy/ext/sdf/_sdf.pyx",
                                          "glumpy/ext/sdf/sdf.c"],
                                 include_dirs=[numpy.get_include()])],
)
