# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
"""
Unimarker collection is a collection of markers of the same type.
"""

import os
import numpy as np
from functools import reduce
from glumpy import gl
from glumpy.gloo.program import Program
from . collection import Collection



class UnimarkerCollection(Collection):
    def __init__(self, marker='cross', **kwargs):

        dtype = [ ('position',    (np.float32, 3), '!local', (0,0,0)),
                  ('size',        (np.float32, 1), 'local', 1),
                  ('orientation', (np.float32, 1), 'local', 0),
                  ('fg_color',    (np.float32, 4), 'local', (0,0,0,1)),
                  ('bg_color',    (np.float32, 4), 'local', (1,1,1,1)),
                  ('linewidth',   (np.float32, 1), 'global', 1.0),
                  ('antialias',   (np.float32, 1), 'global', 1.0) ]

        vertex = get('collections/marker.vert')
        fragment = get('markers/marker-%s.frag' % marker)
        fragment += get('antialias/outline.frag')
        fragment += get('collections/marker.frag')

        Collection.__init__(self, dtype=dtype, itype=None, mode=gl.GL_POINTS,
                            vertex=vertex, fragment=fragment, **kwargs)


    def append(self, count, itemsize=1, **kwargs):
        if count <= 0:
            return

        # defaults = MarkerCollection.defaults
        V = np.zeros(count, dtype=self.vtype)
        for name in self.vtype.names:
            if name not in ["collection_index"]:
                V[name] = kwargs.get(name, self._defaults[name])
        if self.utype:
            U = np.zeros(count, dtype=self.utype)
            for name in self.utype.names:
                if name not in ["__unused__"]:
                    U[name] = kwargs.get(name, self._defaults[name])
        else:
            U = None
        Collection.append(self, vertices=V, uniforms=U, itemsize=itemsize)
