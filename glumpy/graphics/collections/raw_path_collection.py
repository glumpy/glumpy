# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import gl, library
from glumpy.transforms import Position, Viewport
from  . collection import Collection


class RawPathCollection(Collection):
    """
    """

    def __init__(self, user_dtype=None, transform=None, viewport=None,
                 vertex = None, fragment = None, **kwargs):

        """
        Initialize the collection.

        Parameters
        ----------

        user_dtype: list
            The base dtype can be completed (appended) by the used_dtype. It
            only make sense if user also provide vertex and/or fragment shaders

        viewport: glumpy.Transforms
            The viewport to use to render the collection

        transform: glumpy.Tranforms
            The default vertex shader apply the supplied transform to the
            vertices positions before computing the actual vertices positions
            for path thickness. Note that it is necessary to add the
            glumpy.transforms.Viewport transform at the end of the supplied transform.

        vertex: string
            Vertex shader code

        fragment: string
            Fragment  shader code

        color : string
            'local', 'shared' or 'global'
        """

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



    def append(self, P, closed=False, itemsize=None, **kwargs):
        """
        Append a new set of vertices to the collection.

        For kwargs argument, n is the number of vertices (local) or the number
        of item (shared)

        Parameters
        ----------

        P : np.array
            Vertices positions of the path(s) to be added

        closed: bool
            Whether path(s) is/are closed

        itemsize: int or None
            Size of an individual path

        color : list, array or 4-tuple
           Path color
        """

        itemsize  = itemsize or len(P)
        itemcount = len(P)//itemsize
        P = P.reshape(itemcount,itemsize,3)
        if closed:
            V = np.empty((itemcount,itemsize+3), dtype=self.vtype)
            # Apply default values on vertices
            for name in self.vtype.names:
                if name not in ['collection_index', 'position']:
                    V[name][1:-2] = kwargs.get(name, self._defaults[name])
            V["position"][:,1:-2] = P
            V["position"][:,  -2] = V["position"][:,1]
        else:
            V = np.empty((itemcount,itemsize+2), dtype=self.vtype)
            # Apply default values on vertices
            for name in self.vtype.names:
                if name not in ['collection_index', 'position']:
                    V[name][1:-1] = kwargs.get(name, self._defaults[name])
            V["position"][:,1:-1] = P
        V["id"] = 1
        V[:, 0] = V[:, 1]
        V[:,-1] = V[:,-2]
        V["id"][:, 0] = 0
        V["id"][:,-1] = 0

        # Uniforms
        if self.utype:
            U = np.zeros(itemcount, dtype=self.utype)
            for name in self.utype.names:
                if name not in ["__unused__"]:
                    U[name] = kwargs.get(name, self._defaults[name])
        else:
            U = None

        Collection.append(self, vertices=V, uniforms=U,
                                itemsize=itemsize+2+closed)
