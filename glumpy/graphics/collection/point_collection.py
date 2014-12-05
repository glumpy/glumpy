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


class PointCollection(Collection):

    def __init__(self, vertex=None, fragment=None, transform=None):

        dtype = [ ('position', (np.float32, 3), "!local", (0,0,0)),
                  ('size',     (np.float32, 1), "global", 3.0),
                  ('color',    (np.float32, 4), "global", (1,0,0,1) ) ]
        vertex    = library.get("collections/point.vert")
        fragment  = library.get("collections/point.frag")
        Collection.__init__(self, dtype=dtype, itype=None, mode=gl.GL_POINTS,
                            vertex=vertex, fragment=fragment)
        if transform is not None:
            self._program["transform"] = transform
        else:
            self._program["transform"] = Position3D("position")


    def append(self, count, **kwargs):
        if count <= 0:
            return

        defaults = self._defaults
        V = np.zeros(count, dtype=self.vtype)
        for name in self.vtype.names:
            if name not in ["collection_index"]:
                V[name] = kwargs.get(name, defaults[name])
        if self.utype:
            U = np.zeros(count, dtype=self.utype)
            for name in self.utype.names:
                if name not in ["__unused__"]:
                    U[name] = kwargs.get(name, defaults[name])
        else:
            U = None
        Collection.append(self, vertices=V, uniforms=U, itemsize=1)
