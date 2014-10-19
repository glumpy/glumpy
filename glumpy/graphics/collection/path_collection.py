# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
""" """

import os
import numpy as np

from glumpy import gl
from glumpy.shaders import get_file, get_code
from glumpy.graphics.collection.util import fetchcode
from glumpy.graphics.collection.collection import Collection
from glumpy.gloo.program import Program, VertexBuffer, IndexBuffer



class PathCollection(Collection):
    """ """

    def __init__(self, dtype=[], vertex=None, fragment=None, **kwargs):
        """ """

        dtype = [ ('position', (np.float32, 3), '!local', (0,0,0)),
                  ('color',    (np.float32, 4), 'shared', (1,1,1,1))] + dtype
        vertex = vertex or get_code('line-collection.vert')
        fragment = fragment or get_code('line-collection.frag')
        Collection.__init__(self, dtype, itype=np.uint32, mode=gl.GL_LINES,
                                  vertex=vertex, fragment=fragment, **kwargs)


    def append(self, P, **kwargs):
        """ """

        itemsize = kwargs.get('itemsize', len(P))

        count = len(P)/itemsize

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
            U = np.zeros(count, dtype=self.utype)
            for name in self.utype.names:
                if name not in ["__unused__"]:
                    if name in kwargs.keys() or name in defaults.keys():
                        U[name] = kwargs.get(name, defaults[name])
        else:
            U = None


        Collection.append(self, vertices=V, indices=I, uniforms=U, itemsize=itemsize)
