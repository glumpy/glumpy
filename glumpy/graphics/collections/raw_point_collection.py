# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
"""
Raw Point Collection

This collection provides very fast points. Output quality is ugly so it must be
used at small size only (2/3 pixels). You've been warned.
"""

import numpy as np
from glumpy import gl, library
from . collection import Collection
from glumpy.transforms import Position, Viewport


class RawPointCollection(Collection):
    """
    Raw Point Collection

    This collection provides very fast points. Output quality is ugly so it
    must be used at small size only (2/3 pixels). You've been warned.
    """

    def __init__(self, user_dtype=None, transform=None, viewport=None,
                 vertex=None, fragment=None, **kwargs):
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
            for path thickness.

        vertex: string
            Vertex shader code

        fragment: string
            Fragment  shader code

        color : string
            'local', 'shared' or 'global'
        """
        base_dtype = [ ('position', (np.float32, 3), "!local", (0,0,0)),
                       ('size',     (np.float32, 1), "global", 3.0),
                       ('color',    (np.float32, 4), "global", (0,0,0,1) ) ]

        dtype = base_dtype
        if user_dtype:
            dtype.extend(user_dtype)

        if vertex is None:
            vertex = library.get("collections/raw-point.vert")
        if fragment is None:
            fragment= library.get("collections/raw-point.frag")

        Collection.__init__(self, dtype=dtype, itype=None, mode=gl.GL_POINTS,
                            vertex=vertex, fragment=fragment, **kwargs)

        # Set hooks if necessary
        program = self._programs[0]

        if "transform" in program.hooks:
            if transform is not None:
                # FIXME: this line break things because snippet code will be included
                #        and it messes with new snippet code
                # program["transform"] = Position()
                program["transform"] = transform
            else:
                program["transform"] = Position()

        if "viewport" in program.hooks:
            if viewport is not None:
                # FIXME: this line break things because snippet code will be included
                #        and it messes with new snippet code
                # program["viewport"] = Viewport()
                program["viewport"] = viewport
            else:
                program["viewport"] = Viewport()



    def append(self, P, itemsize=None, **kwargs):
        """
        Append a new set of vertices to the collection.

        For kwargs argument, n is the number of vertices (local) or the number
        of item (shared)

        Parameters
        ----------

        P : np.array
            Vertices positions of the points(s) to be added

        itemsize: int or None
            Size of an individual path

        color : list, array or 4-tuple
           Path color
        """

        itemsize  = itemsize or 1
        itemcount = len(P)/itemsize

        V = np.empty(len(P), dtype=self.vtype)

        # Apply default values on vertices
        for name in self.vtype.names:
            if name not in ['position', "collection_index"]:
                V[name] = kwargs.get(name, self._defaults[name])
        V["position"] = P

        # Uniforms
        if self.utype:
            U = np.zeros(itemcount, dtype=self.utype)
            for name in self.utype.names:
                if name not in ["__unused__"]:
                    U[name] = kwargs.get(name, self._defaults[name])
        else:
            U = None

        Collection.append(self, vertices=V, uniforms=U, itemsize=itemsize)
