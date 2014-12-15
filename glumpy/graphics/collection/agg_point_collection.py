# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
""" """

import numpy as np
from glumpy import gl, library
from glumpy.transforms import Position3D
from glumpy.graphics.collection.collection import Collection


class AggPointCollection(Collection):

    def __init__(self, transform=None, **kwargs):

        dtype = [ ('position', (np.float32, 3), "!local", (0,0,0)),
                  ('size',     (np.float32, 1), "global", 3.0),
                  ('color',    (np.float32, 4), "global", (1,0,0,1) ) ]

        vertex    = library.get("collections/agg-point.vert")
        fragment  = library.get("collections/agg-point.frag")

        Collection.__init__(self, dtype=dtype, itype=None, mode=gl.GL_POINTS,
                            vertex=vertex, fragment=fragment, **kwargs)
        if transform is not None:
            self._program["transform"] = transform
        else:
            self._program["transform"] = Position3D()


    def append(self, P, **kwargs):
        """ """
        V = self.bake(P)
        U = np.zeros(len(P), dtype=self.utype) if self.utype else None
        self.apply_defaults(V, U, protect=["position"], **kwargs)
        Collection.append(self, vertices=V, uniforms=U, itemsize=1)


    def bake(self, P):
        """ """
        V = np.empty(len(P), dtype=self.vtype)
        V["position"] = P
        return V
