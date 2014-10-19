# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
""" """

import numpy as np
from glumpy import gl
from glumpy.shaders import get_file, get_code
from glumpy.graphics.collection.collection import Collection



class LineCollection(Collection):
    """ """

    def __init__(self, dtype=[], vertex=None, fragment=None, **kwargs):
        """ """

        dtype = [ ('position', (np.float32, 3), '!local', (0,0,0)),
                  ('color',    (np.float32, 4), 'shared', (1,1,1,1))] + dtype
        vertex = vertex or get_code('line.vert')
        fragment = fragment or get_code('line.frag')

        Collection.__init__(self, dtype, itype=np.uint32, mode=gl.GL_LINES,
                                  vertex=vertex, fragment=fragment, **kwargs)


    def append(self, P, **kwargs):
        """ """

        itemsize = kwargs.get('itemsize', len(P))

        V = np.zeros(len(P), dtype=self.vtype)
        V['position'] = P
        I = np.repeat(np.arange(itemsize),2)[1:-1]

        defaults = self._defaults
        reserved = ["collection_index", "position"]
        for name in self.vtype.names:
            if name not in reserved:
                if name in kwargs.keys() or name in defaults.keys():
                    V[name] = kwargs.get(name, defaults[name])

        if self.utype:
            U = np.zeros(1, dtype=self.utype)
            for name in self.utype.names:
                if name not in ["__unused__"]:
                    if name in kwargs.keys() or name in defaults.keys():
                        U[name] = kwargs.get(name, defaults[name])
        else:
            U = None


        Collection.append(self, vertices=V, indices=I ,uniforms=U, itemsize=itemsize)
