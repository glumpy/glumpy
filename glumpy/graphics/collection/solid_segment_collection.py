# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
""" """

import os
import numpy as np
from functools import reduce
from glumpy import gl
from glumpy.gloo.program import Program
from glumpy.graphics.collection.util import fetchcode
from glumpy.graphics.collection.collection import Collection



class SolidSegmentCollection(Collection):
    """ """

    defaults = { 'P0'          : (0.0,0.0),
                 'P1'          : (0.0,0.0),
                 'index'       : 0.0,
                 'fg_color'    : (0,0,0,1),
                 'antialias'   : 1.0,
                 'linewidth'   : 1.0 }

    def __init__(self, P0=None, P1=None, **kwargs):
        """
        """

        # This cannot be changed (shader code depends on it)
        dtypes = [ ('P0',          np.float32, 2),
                   ('P1',          np.float32, 2),
                   ('index',       np.float32, 1),
                   ('fg_color',    np.float32, 4),
                   ('linewidth',   np.float32, 1),
                   ('antialias',   np.float32, 1) ]

        # This can be changed but 'P0', 'P1' and 'index' that must be local
        scopes = { 'P0'         : 'local',
                   'P1'         : 'local',
                   'index'      : 'local',
                   'fg_color'   : 'local',
                   'linewidth'  : 'global',
                   'antialias'  : 'global' }
        # Override kwargs (these cannot be changed)
        kwargs['P0'] = 'local'
        kwargs['P1'] = 'local'
        kwargs['index'] = 'local'

        Collection.__init__(self, dtypes, scopes, itype=np.uint32, **kwargs)

        path = os.path.dirname(__file__)
        path = os.path.join(path,'shaders')
        vertex = ""
        if self.utype is not None:
            vertex += fetchcode(self.utype)
        else:
            vertex += "void fetch_uniforms(void) { }\n"
        vertex += self._declarations["uniforms"]
        vertex += self._declarations["attributes"]
        vertex += open(os.path.join(path, 'solid-segment.vert')).read()

        fragment = ""
        fragment += open(os.path.join(path, 'antialias.glsl')).read()
        fragment += open(os.path.join(path, 'solid-segment.frag')).read()

        # self.append(P0, P1)

        self._program = Program(vertex, fragment)
        for name in self._uniforms.keys():
            self._uniforms[name] = SolidSegmentCollection.defaults.get(name)
            self._program[name] = self._uniforms[name]
        self._build_buffers()



    def append(self, P0, P1, **kwargs):
        """ """

        defaults = SolidSegmentCollection.defaults
        count = len(P0)
        V = np.zeros(count, dtype=self.vtype)
        for name in self.vtype.names:
            V[name] = kwargs.get(name, defaults[name])
        if self.utype:
            U = np.zeros(count, dtype=self.utype)
            for name in self.utype.names:
                U[name] = kwargs.get(name, defaults[name])
        else:
            U = None

        V['P0'] = P0
        V['P1'] = P1
        V = V.repeat(4,axis=0)
        V['index'] = np.resize([0,1,2,3], 4*count)
        I = np.resize( np.array([0,1,2,0,2,3], dtype=np.uint32), 6*count)
        I += np.repeat( 4*np.arange(count), 6)
        Collection.append(self, vertices=V, uniforms=U, indices=I)



    def draw(self):
        """ """

        Collection.draw(self, gl.GL_TRIANGLES)
