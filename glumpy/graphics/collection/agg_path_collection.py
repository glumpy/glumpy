# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
""" """

import numpy as np
from glumpy import gl, gloo
from glumpy.shaders import get_file, get_code
from glumpy.graphics.collection.collection import Collection



class AggPathCollection(Collection):
    """ """

    def __init__(self, **kwargs):

        dtype = [ ('position',    (np.float32, 2), '!local', (0,0,0)),
                  ('linewidth',   (np.float32, 1), 'shared', 1.0),
                  ('antialias',   (np.float32, 1), 'shared', 1.0),
                  ('miter_limit', (np.float32, 1), 'global', 4.0),
                  ('jointype',    (np.float32, 1), 'shared', 0.0),
                  ('captype',     (np.float32, 1), 'shared', 0.0),
                  ('color',       (np.float32, 4), 'shared', (0,0,0,1))]

        vertex = get_code('collections/agg-path.vert')
        fragment = get_code('collections/agg-path.frag')
        geometry = gloo.GeometryShader(get_code('collections/agg-path.geom'),
                                       4, gl.GL_LINES_ADJACENCY_EXT, gl.GL_TRIANGLE_STRIP)
        Collection.__init__(self, dtype, itype=np.uint32,
                                  mode=gl.GL_LINE_STRIP_ADJACENCY_EXT,
                                  vertex=vertex, fragment=fragment, geometry=geometry,
                                  **kwargs)


    def append(self, P, closed=False, **kwargs):
        """ """

        if closed:
            if np.allclose(P[0],P[1]):
                #I = (np.arange(len(P)+2)-1)
                #I[0], I[-1] = 0, len(P)-1
                I = (np.arange(len(P)+4)-2)
                I[0], I[1], I[-2], I[-1] = 0, 0, len(P)-1, len(P)-1
            else:
                #I = (np.arange(len(P)+3)-1)
                #I[0], I[-2], I[-1] = len(P)-1, 0, 1
                I = (np.arange(len(P)+5)-2)
                I[0], I[1], I[-3], I[-2], I[-1] = len(P)-1,len(P)-1, 0, 1, 1
        else:
            I = (np.arange(len(P)+4)-2)
            I[0], I[1], I[-2], I[-1] = 0, 0, len(P)-1, len(P)-1

        I = I.astype(np.uint32).view(gloo.IndexBuffer)

        itemsize = kwargs.get('itemsize', len(P))

        V = np.zeros(len(P), dtype=self.vtype)
        V['position'] = P
        # I = np.repeat(np.arange(itemsize),2)[1:-1]

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
