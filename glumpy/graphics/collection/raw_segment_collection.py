# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------

import numpy as np
from glumpy import gl, library
from glumpy.transforms import Position3D
from glumpy.graphics.collection.collection import Collection


class RawSegmentCollection(Collection):

    def __init__(self, transform=None, **kwargs):

        dtype = [ ('P',     (np.float32, 3), '!local', (0,0,0)),
                  ('color', (np.float32, 4), 'global', (0,0,0,1)) ]

        vertex = library.get('collections/raw-segment.vert')
        fragment = library.get('collections/raw-segment.frag')
        Collection.__init__(self, dtype=dtype, itype=None, mode=gl.GL_LINES,
                            vertex=vertex, fragment=fragment, **kwargs)
        if transform is not None:
            self._program["transform"] = transform
        else:
            self._program["transform"] = Position3D()


    def append(self, P0, P1, **kwargs):

        V = self.bake(P0, P1)
        U = np.zeros(len(P0), dtype=self.utype) if self.utype else None
        protect = ["P"]
        self.apply_defaults(V, U, protect=protect, **kwargs)
        Collection.append(self, vertices=V, uniforms=U)


    def bake(self, P0, P1):
        V = np.zeros(2*len(P0), dtype=self.vtype)
        V['P'][0::2] = P0
        V['P'][1::2] = P1
        return V
