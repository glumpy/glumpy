# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import numpy as np
stride_tricks = np.lib.stride_tricks

from glumpy import gl, library
from glumpy.transforms import Position3D
from glumpy.graphics.collection.collection import Collection


class AggPathCollection(Collection):
    """
    """

    def __init__(self, vertex=None, fragment=None, transform=None, **kwargs):
        dtype = [ ('p0',         (np.float32, 3), '!local', (0,0,0)),
                  ('p1',         (np.float32, 3), '!local', (0,0,0)),
                  ('p2',         (np.float32, 3), '!local', (0,0,0)),
                  ('p3',         (np.float32, 3), '!local', (0,0,0)),
                  ('uv',         (np.float32, 2), '!local', (0,0)),
                  ('caps',       (np.float32, 2), 'global', (0,0)),
                  ('join',       (np.float32, 1), 'global', 0),
                  ('color',      (np.float32, 4), 'global', (0,0,0,1)),
                  ('miter_limit',(np.float32, 1), 'global', 4),
                  ('linewidth',  (np.float32, 1), 'global', 1),
                  ('antialias',  (np.float32, 1), 'global', 1) ]

        vertex = library.get('collections/agg-path.vert')
        fragment = library.get('collections/agg-path.frag')

        Collection.__init__(self, dtype=dtype, itype=np.uint32, mode=gl.GL_TRIANGLES,
                            vertex=vertex, fragment=fragment, **kwargs)

        if transform is not None:
            self._program["transform"] = transform
        else:
            self._program["transform"] = Position3D("position")


    def append(self, P, closed=False, **kwargs):
        """ """

        V,I = self.bake(P, closed=closed)
        U = np.zeros(1, dtype=self.utype) if self.utype else None

        protect = ["p0", "p1", "p2", "p3", "uv"]
        self.apply_defaults(V, U, protect=protect, **kwargs)
        Collection.append(self, vertices=V, uniforms=U, indices=I)


    def bake(self, P, closed=False):
        """ """

        n = len(P)
        I = np.arange(n, dtype=np.uint32)
        I = stride_tricks.as_strided(I,(n-3,4),(4,4))

        V = np.empty(n-1, dtype=self.vtype)
        PI = P[I]

        if closed:
            V['p0'][0] = P[-1]
        else:
            V['p0'][0] = P[0]
        V['p1'][0] = P[0]
        V['p2'][0] = P[1]
        V['p3'][0] = P[2]

        V['p0'][1:-1] = PI[:,0]
        V['p1'][1:-1] = PI[:,1]
        V['p2'][1:-1] = PI[:,2]
        V['p3'][1:-1] = PI[:,3]

        V['p0'][-1] = P[-3]
        V['p1'][-1] = P[-2]
        V['p2'][-1] = P[-1]
        if closed:
            V['p3'][-1] = P[0]
        else:
            V['p3'][-1] = P[-1]

        V = np.repeat(V, 4, axis=0).reshape((len(V),4))
        V['uv'] = (-1,-1), (-1,+1), (+1,-1), (+1,+1)

        if closed:
            I = np.resize(np.array([0,1,2, 1,2,3], dtype=np.uint32),(n)*(2*3))
            I += np.repeat( 4*np.arange(n), 6)
            I[-6:] = 4*n-6,4*n-5,0,4*n-5,0,1
            print len(V.ravel())
        else:
            I = np.resize(np.array([0,1,2, 1,2,3], dtype=np.uint32),(n-1)*(2*3))
            I += np.repeat( 4*np.arange(n-1), 6)

        return V.ravel(), I.ravel()
