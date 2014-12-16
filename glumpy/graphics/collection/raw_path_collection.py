# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import gl, library
from glumpy.transforms import Position3D
from glumpy.graphics.collection.collection import Collection


class RawPathCollection(Collection):
    """
    """

    def __init__(self, transform=None, **kwargs):
        dtype = [('position', (np.float32, 3), '!local', (0,0,0)),
                 ('id',       (np.float32, 1), '!local', 0),
                 ('color',    (np.float32, 4), 'local', (0,0,0,1)) ]

        vertex = library.get('collections/raw-path.vert')
        fragment = library.get('collections/raw-path.frag')

        Collection.__init__(self, dtype=dtype, itype=None, mode=gl.GL_LINE_STRIP,
                            vertex=vertex, fragment=fragment, **kwargs)

        if transform is not None:
            self._program["transform"] = transform
        else:
            self._program["transform"] = Position3D()


    def append(self, P, closed=False, **kwargs):
        """ """
        V = self.bake(P, closed=closed)
        U = np.zeros(1, dtype=self.utype) if self.utype else None
        protect = ["position", "id"]
        self.apply_defaults(V, U, protect=protect, **kwargs)
        Collection.append(self, vertices=V, uniforms=U)


    def bake(self, P, closed=True):
        """ """
        n = len(P)
        if closed:
            V = np.empty(n+3, dtype=self.vtype)
            V["position"][1:-2] = P
            V["position"][-2] = P[0]
        else:
            V = np.empty(n+2, dtype=self.vtype)
            V["position"][1:-1] = P

        V["id"] = 1
        V[0] = V[1]
        V[-1] = V[-2]
        V["id"][0] = 0
        V["id"][-1] = 0

        return V
