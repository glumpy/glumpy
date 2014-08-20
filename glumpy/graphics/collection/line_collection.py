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



class LineCollection(Collection):
    """ """

    # This cannot be changed (shader code depends on it)
    dtypes = [ ('position',  np.float32, 3),
               ('color',     np.float32, 4) ]

    # Default variable scopes
    scopes = { 'position'   : '!local',
               'color'      : 'shared' }

    # Default variable values
    defaults = { 'position' : (0,0,0),
                 'color'    : (1,1,1,1) }

    def __init__(self, **kwargs):
        """ """

        # Extend dtypes with user argument
        dtypes = list(LineCollection.dtypes)
        if "dtypes" in kwargs.keys():
            dtypes.extend(kwargs.get("dtypes", []))
            del kwargs["dtypes"]

        scopes = dict(LineCollection.scopes)
        if "scopes" in kwargs.keys():
            scopes.update(kwargs.get("scopes", {}))
            del kwargs["scopes"]


        # Initialize collection
        Collection.__init__(self, dtypes, scopes, itype=np.uint32, **kwargs)

        # Set draw mode
        self._mode = gl.GL_LINES

        # Build program
        user_vertex = kwargs.get("vertex", None)
        user_fragment = kwargs.get("fragment", None)

        vertex = ""
        if self.utype is not None:
            vertex += fetchcode(self.utype)
        else:
            vertex += "void fetch_uniforms(void) { }\n"
        vertex += self._declarations["uniforms"]
        vertex += self._declarations["attributes"]
        if user_vertex is None:
            vertex += get_code('line-collection.vert')
        else:
            vertex += user_vertex
        if user_fragment is None:
            fragment = get_code('line-collection.frag')
        else:
            fragment = user_fragment


        self._program = Program(vertex, fragment)
        for name in self._uniforms.keys():
            self._uniforms[name] = LineCollection.defaults.get(name)
            self._program[name] = self._uniforms[name]
        self._build_buffers()



    def append(self, P, **kwargs):
        """ """

        itemsize = kwargs.get('itemsize', len(P))

        V = np.zeros(len(P), dtype=self.vtype)
        V['position'] = P
        I = np.repeat(np.arange(itemsize),2)[1:-1]

        defaults = LineCollection.defaults
        reserved = ["a_uniform_index", "position"]
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
