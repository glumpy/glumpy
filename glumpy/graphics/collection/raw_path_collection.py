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

    def __init__(self, user_dtype=None, transform=None,
                 vertex = None, fragment = None, **kwargs):

        base_dtype = [('position', (np.float32, 3), '!local', (0,0,0)),
                      ('id',       (np.float32, 1), '!local', 0),
                      ('color',    (np.float32, 4), 'local', (0,0,0,1)) ]

        dtype = base_dtype
        if user_dtype:
            dtype.extend(user_dtype)

        if vertex is None:
            vertex = library.get('collections/raw-path.vert')
        if fragment is None:
            fragment = library.get('collections/raw-path.frag')

        Collection.__init__(self, dtype=dtype, itype=None, mode=gl.GL_LINE_STRIP,
                            vertex=vertex, fragment=fragment, **kwargs)

        # Set hooks if necessary
        if "transform" in self._program._hooks.keys():
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


    def bake(self, P, closed=False):
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

    # Old path
    # -------------
    # def append(self, P, **kwargs):
    #     """ """

    #     itemsize = kwargs.get('itemsize', len(P))
    #     count = len(P)/itemsize

    #     V = np.zeros(len(P), dtype=self.vtype)
    #     V['position'] = P
    #     I = np.repeat(np.arange(itemsize),2)[1:-1]

    #     defaults = self._defaults
    #     reserved = ["collection_index", "position"]
    #     for name in self.vtype.names:
    #         if name not in reserved:
    #             if name in kwargs.keys() or name in defaults.keys():
    #                 V[name] = kwargs.get(name, defaults[name])
    #     if self.utype:
    #         U = np.zeros(count, dtype=self.utype)
    #         for name in self.utype.names:
    #             if name not in ["__unused__"]:
    #                 if name in kwargs.keys() or name in defaults.keys():
    #                     U[name] = kwargs.get(name, defaults[name])
    #     else:
    #         U = None


    #     Collection.append(self, vertices=V, indices=I, uniforms=U, itemsize=itemsize)
