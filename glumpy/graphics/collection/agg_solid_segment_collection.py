# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------

import numpy as np
from glumpy import gl, library
from glumpy.transforms import Position2D
from glumpy.graphics.collection.collection import Collection


class AggSolidSegmentCollection(Collection):

    def __init__(self, vertex=None, fragment=None, transform=None, **kwargs):

        dtype = [ ('P0',        (np.float32, 2), '!local', (0,0)),
                  ('P1',        (np.float32, 2), '!local', (0,0)),
                  ('index',     (np.float32, 1), '!local', 0),
                  ('color',     (np.float32, 4), 'shared', (0,0,0,1)),
                  ('linewidth', (np.float32, 1), 'shared', 1),
                  ('antialias', (np.float32, 1), 'shared', 1) ]

        dtype = [ ('P0',        (np.float32, 3), '!local', (0,0,0)),
                  ('P1',        (np.float32, 3), '!local', (0,0,0)),
                  ('index',     (np.float32, 1), '!local', 0),
                  ('color',     (np.float32, 4), 'shared', (0,0,0,1)),
                  ('linewidth', (np.float32, 1), 'shared', 1),
                  ('antialias', (np.float32, 1), 'shared', 1) ]

        vertex = library.get('collections/agg-solid-segment.vert')
        fragment = library.get('collections/agg-solid-segment.frag')
        Collection.__init__(self, dtype=dtype, itype=np.uint32, mode=gl.GL_TRIANGLES,
                            vertex=vertex, fragment=fragment, **kwargs)
        if transform is not None:
            self._program["transform"] = transform
        else:
            self._program["transform"] = Position2D("position")


    def append(self, P0, P1, **kwargs):
        """ """

        count = len(P0)
        V = np.zeros(count, dtype=self.vtype)

        defaults = self._defaults
        reserved = ["collection_index", "P0", "P1", "index"]

        for name in self.vtype.names:
            if name not in reserved:
                V[name] = kwargs.get(name, defaults[name])
        if self.utype:
            U = np.zeros(count, dtype=self.utype)
            for name in self.utype.names:
                if name not in ["__unused__"]:
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
