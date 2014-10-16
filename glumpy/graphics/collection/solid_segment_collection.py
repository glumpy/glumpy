# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
""" """

import numpy as np
from glumpy import gl
from glumpy.shaders import get
from glumpy.gloo.program import Program
from glumpy.graphics.collection.util import fetchcode
from glumpy.graphics.collection.collection import Collection



class SolidSegmentCollection(Collection):

    def __init__(self, P0=None, P1=None, **kwargs):

        dtype = [ ('P0',          (np.float32, 2), '!local', (0,0)),
                  ('P1',          (np.float32, 2), '!local', (0,0)),
                  ('index',       (np.float32, 1), '!local', 0),
                  ('fg_color',    (np.float32, 4), 'global', (0,0,0,1)),
                  ('linewidth',   (np.float32, 1), 'global', 1),
                  ('antialias',   (np.float32, 1), 'global', 1) ]

        vertex = get('solid-segment.vert')
        fragment = get('antialias/stroke.frag')
        fragment += get('antialias/cap.frag')
        fragment += get('solid-segment.frag')

        Collection.__init__(self, dtype=dtype, itype=np.uint32, mode=gl.GL_TRIANGLES,
                            vertex=vertex, fragment=fragment, **kwargs)

    def append(self, P0, P1, **kwargs):
        """ """

        defaults = self._defaults
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
