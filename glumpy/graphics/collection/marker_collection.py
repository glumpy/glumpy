# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
"""
Marker collection is a collection of markers of different types.
"""
import numpy as np
from glumpy import gl, library
from glumpy.transforms import Position3D
from glumpy.graphics.collection.collection import Collection


class MarkerCollection(Collection):
    def __init__(self, marker = 'spade', transform=None, **kwargs):
        dtype = [ ('position',    (np.float32, 3), '!local', (0,0,0)),
                  ('size',        (np.float32, 1), 'local', 1),
                  ('marker',      (np.float32, 1), 'local', 1),
                  ('orientation', (np.float32, 1), 'local', 0.0),
                  ('fg_color',    (np.float32, 4), 'local', (0,0,0,1)),
                  ('bg_color',    (np.float32, 4), 'local', (1,1,1,1)),
                  ('linewidth',   (np.float32, 1), 'global', 1.0),
                  ('antialias',   (np.float32, 1), 'global', 1.0) ]

        vertex   = library.get('collections/marker.vert')
        fragment = library.get('collections/marker.frag')
        Collection.__init__(self, dtype=dtype, itype=None, mode=gl.GL_POINTS,
                            vertex=vertex, fragment=fragment, **kwargs)

        if transform is not None:
            self._program["transform"] = transform
        else:
            self._program["transform"] = Position3D()

        self._program["marker"] = marker
        self._program["paint"] = "outline"


    def append(self, P, **kwargs):
        V = np.zeros(len(P), dtype=self.vtype)
        U = np.zeros(len(P), dtype=self.utype) if self.utype else None
        self.apply_defaults(V, U, **kwargs)
        V["position"] = P
        Collection.append(self, vertices=V, uniforms=U, itemsize=1)
