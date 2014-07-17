# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
""" """

import os
import numpy as np
from functools import reduce
from glumpy.gloo.program import Program
from glumpy.graphics.collection.util import fetchcode
from glumpy.graphics.collection.collection import Collection



class MarkerCollection(Collection):
    """ """

    defaults = { 'position'    : (0.0,0.0,0.0),
                 'size'        : 32.0,
                 'orientation' : 0.0,
                 'fg_color'    : (0,0,0,1),
                 'bg_color'    : (1,1,1,1),
                 'antialias'   : 1.0,
                 'linewidth'   : 1.0 }

    def __init__(self, count=0, marker='cross', **kwargs):
        # This cannot be changed (shader code depends on it)
        dtypes = [ ('position',    np.float32, 3),
                   ('size',        np.float32, 1),
                   ('orientation', np.float32, 1),
                   ('fg_color',    np.float32, 4),
                   ('bg_color',    np.float32, 4),
                   ('linewidth',   np.float32, 1),
                   ('antialias',   np.float32, 1) ]

        # This can be changed but 'position' that must be local
        scopes = { 'position'   : 'local',
                   'size'       : 'local',
                   'orientation': 'local',
                   'fg_color'   : 'local',
                   'bg_color'   : 'local',
                   'linewidth'  : 'global',
                   'antialias'  : 'global' }
        kwargs['position'] = 'local'


        Collection.__init__(self, dtypes, scopes, **kwargs)

        path = os.path.dirname(__file__)
        path = os.path.join(path,'shaders')
        vertex = ""
        if self.utype is not None:
            vertex += fetchcode(self.utype)
        else:
            vertex += "void fetch_uniforms(void) { }\n"
        vertex += self._declarations["uniforms"]
        vertex += self._declarations["attributes"]
        vertex += open(os.path.join(path, 'marker.vert')).read()

        fragment = ""
        fragment += open(os.path.join(path, 'marker-%s.frag') % marker).read()
        fragment += open(os.path.join(path, 'antialias.glsl')).read()
        fragment += open(os.path.join(path, 'marker.frag')).read()

        if count > 0:
            V = np.zeros(count, dtype = self.vtype)
            Collection.append(self, V, itemsize=1)

        self._program = Program(vertex, fragment)
        for name in self._uniforms.keys():
            self._uniforms[name] = MarkerCollection.defaults.get(name)
            self._program[name] = self._uniforms[name]
        self._build_buffers()



    # def append( self, position, size=32.0, orientation = 0.0,
    #                   fg_color = (0,0,0,1), bg_color = (1,1,1,1),
    #                   linewidth = 1.0, antialias = 1.0):
    #     V = np.zeros(1, dtype=self.vtype)
    #     V['position'] = position
    #     V['orientation'] = orientation
    #     V['size'] = 32
    #     U = np.zeros(1, dtype=self._uniforms.dtype)
    #     U['fg_color'] = 0,0,0,1
    #     U['bg_color'] = 0,0,0,1
    #     Collection.append(self, V, U)


    def draw(self, *args, **kwargs):
        self._program.draw(*args, **kwargs)
