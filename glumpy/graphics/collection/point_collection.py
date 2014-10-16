# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
""" """

import numpy as np
from glumpy import gl
from glumpy.gloo.program import Program
from glumpy.shaders import get_file, get_code
from glumpy.graphics.collection.util import fetchcode
from glumpy.graphics.collection.collection import Collection



class PointCollection(Collection):
    """ """

    # This cannot be changed (shader code depends on it)
    dtypes = [ ('position',    np.float32, 3),
               ('size',        np.float32, 1) ]

    # This can be changed but 'position' that must be local
    scopes = { 'position'   : '!local',
               'size'       : 'local' }

    # Default variable values
    defaults = { 'position'    : (0.0,0.0,0.0),
                 'size'        : 32.0}

    def __init__(self, **kwargs):

        # Extend dtypes with user argument
        dtypes = list(PointCollection.dtypes)
        if "dtypes" in kwargs.keys():
            dtypes.extend(kwargs.get("dtypes", []))
            del kwargs["dtypes"]
        scopes = dict(PointCollection.scopes)

        # Initialize collection
        Collection.__init__(self, dtypes, scopes, itype=None, **kwargs)

        # Set draw mode
        self._mode = gl.GL_POINTS

        # Build vertex code
        user_vertex = kwargs.get("vertex", None)
        vertex = ""
        if self.utype is not None:
            vertex += fetchcode(self.utype)
        else:
            vertex += "void fetch_uniforms(void) { }\n"
        vertex += self._declarations["uniforms"]
        vertex += self._declarations["attributes"]
        if user_vertex is None:
            vertex += get_code('collections/point.vert')
        else:
            vertex += user_vertex

        # Build fragment code
        user_fragment = kwargs.get("fragment", None)
        if user_fragment is None:
            fragment = get_code('collections/point.frag')
        else:
            fragment = user_fragment

        # Build program
        self._program = Program(vertex, fragment)

        # Initialize uniforms
        for name in self._uniforms.keys():
            self._uniforms[name] = PointCollection.defaults.get(name)
            self._program[name] = self._uniforms[name]

        # Build buffers
        self._build_buffers()



    def append(self, count, itemsize=1, **kwargs):
        """ """

        if count <= 0:
            return

        defaults = PointCollection.defaults
        V = np.zeros(count, dtype=self.vtype)
        for name in self.vtype.names:
            if name not in ["a_uniform_index"]:
                V[name] = kwargs.get(name, defaults[name])
        if self.utype:
            U = np.zeros(count, dtype=self.utype)
            for name in self.utype.names:
                if name not in ["__unused__"]:
                    U[name] = kwargs.get(name, defaults[name])
        else:
            U = None
        Collection.append(self, vertices=V, uniforms=U, itemsize=itemsize)
