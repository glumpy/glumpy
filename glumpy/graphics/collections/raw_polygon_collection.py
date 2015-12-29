# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
import triangle

from glumpy import gl, library
from glumpy.transforms import Position
from . collection import Collection


def triangulate(vertices):
    n = len(vertices)
    vertices = np.array(vertices)
    zmean = vertices[:,2].mean()
    vertices_2d = vertices[:,:2]
    segments = np.repeat(np.arange(n+1),2)[1:-1]
    segments[-2:] = n-1,0
    T = triangle.triangulate({'vertices': vertices_2d,
                              'segments': segments}, "p")
    vertices_2d = T["vertices"]
    triangles   = T["triangles"]
    vertices = np.empty((len(vertices_2d),3))
    vertices[:,:2] = vertices_2d
    vertices[:,2] = zmean
    return vertices, triangles


class RawPolygonCollection(Collection):

    def __init__(self, user_dtype=None, transform=None, viewport=None,
                 vertex = None, fragment = None, **kwargs):

        base_dtype = [('position', (np.float32, 3), '!local', (0,0,0)),
                      ('color',    (np.float32, 4), 'local',  (0,0,0,1)) ]

        dtype = base_dtype
        if user_dtype:
            dtype.extend(user_dtype)

        if vertex is None:
            vertex = library.get('collections/raw-triangle.vert')
        if fragment is None:
            fragment = library.get('collections/raw-triangle.frag')

        Collection.__init__(self, dtype=dtype, itype=np.uint32, mode=gl.GL_TRIANGLES,
                            vertex=vertex, fragment=fragment, **kwargs)

        # Set hooks if necessary
        program = self._programs[0]
        if "transform" in program.hooks:
            if transform is not None:
                program["transform"] = transform
            else:
                program["transform"] = Position()

        if "viewport" in program.hooks:
            if viewport is not None:
                program["viewport"] = viewport
            else:
                program["viewport"] = Viewport()



    def append(self, points, **kwargs):
        """
        Append a new set of vertices to the collection.

        For kwargs argument, n is the number of vertices (local) or the number
        of item (shared)

        Parameters
        ----------

        points : np.array
            Vertices composing the triangles

        color : list, array or 4-tuple
           Path color
        """

        vertices, indices = triangulate(points)
        itemsize  = len(vertices)
        itemcount = 1

        V = np.empty(itemcount*itemsize, dtype=self.vtype)
        for name in self.vtype.names:
            if name not in ['collection_index', 'position']:
                V[name] = kwargs.get(name, self._defaults[name])
        V["position"] = vertices

        # Uniforms
        if self.utype:
            U = np.zeros(itemcount, dtype=self.utype)
            for name in self.utype.names:
                if name not in ["__unused__"]:
                    U[name] = kwargs.get(name, self._defaults[name])
        else:
            U = None

        I = np.array(indices).ravel()
        Collection.append(self, vertices=V, uniforms=U, indices=I,
                                itemsize=itemsize)
