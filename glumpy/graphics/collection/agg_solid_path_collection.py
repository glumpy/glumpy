# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import gl, library
from glumpy.transforms import Position3D
from glumpy.graphics.collection.collection import Collection


class AggSolidPathCollection(Collection):
    """
    """

    def __init__(self, vertex=None, fragment=None, transform=None, **kwargs):
        dtype = [ ('prev',       (np.float32, 3), '!local', (0,0,0)),
                  ('curr',       (np.float32, 3), '!local', (0,0,0)),
                  ('next',       (np.float32, 3), '!local', (0,0,0)),
                  ('id',         (np.float32, 1), '!local', 0),
                  ('color',      (np.float32, 4), 'shared', (0,0,0,1)),
                  ('linewidth',  (np.float32, 1), 'shared', 1),
                  ('antialias',  (np.float32, 1), 'shared', 1) ]

        vertex = library.get('collections/agg-solid-path.vert')
        fragment = library.get('collections/agg-solid-path.frag')

        Collection.__init__(self, dtype=dtype, itype=None, mode=gl.GL_TRIANGLE_STRIP,
                            vertex=vertex, fragment=fragment, **kwargs)

        if transform is not None:
            self._program["transform"] = transform
        else:
            self._program["transform"] = Position3D("position")


    def append(self, P, closed=False, **kwargs):

        V = self.bake(P, closed=closed)

        defaults = self._defaults
        reserved = ["collection_index", "prev", "curr", "next", "id"]

        for name in self.vtype.names:
            if name not in reserved:
                V[name] = kwargs.get(name, defaults[name])

        if self.utype:
            U = np.zeros(1, dtype=self.utype)
            for name in self.utype.names:
                if name not in ["__unused__"]:
                    U[name] = kwargs.get(name, defaults[name])
        else:
            U = None

        Collection.append(self, vertices=V, uniforms=U)


    def bake(self, P, closed=True):

        n = len(P)
        if closed:
            R = np.empty(n+3, dtype=self.vtype)
            R_ = R[1:-1]
            R_['curr'][:-1]  = P
            R_['prev'][1:-1] = P[:-1]
            R_['prev'][0]    = P[-1]
            R_['next'][:-2]  = P[1:]
            R_['next'][-2]   = P[0]
            R_[-1]           = R_[0]
        else:
            R = np.empty(n+2, dtype=self.vtype)
            R_ = R[1:-1]
            R_['curr']      = P
            R_['prev'][1:]  = P[:-1]
            R_['prev'][0]   = P[0]
            R_['next'][:-1] = P[1:]
            R_['next'][-1]  = P[-1]
        R = np.repeat(R,2,axis=0)
        R['id'] = np.tile([1,-1],len(R)/2)

        R[:+2] = R[+2:+4]
        R[-2:] = R[-4:-2]
        R[:+2]['id'] = 2,-2
        R[-2:]['id'] = 2,-2

        return R
