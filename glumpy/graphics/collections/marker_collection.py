# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
"""
Antigrain Geometry Marker collection.

This collection provides antialiased and accurate markers with a unique type.
"""
import numpy as np
from glumpy import gl, library
from . collection import Collection
from glumpy.transforms import Position, Viewport


class MarkerCollection(Collection):
    """
    Antigrain Geometry Marker collection.

    This collection provides antialiased and accurate markers with a unique
    type.
    """

    def __init__(self, marker='heart', user_dtype=None, transform=None,
                 viewport=None, vertex=None, fragment=None, **kwargs):
        """
        Initialize the collection.

        Parameters
        ----------

        user_dtype: list
            The base dtype can be completed (appended) by the used_dtype. It
            only make sense if user also provide vertex and/or fragment shaders

        transform: glumpy.Tranforms
            The default vertex shader apply the supplied transform to the
            vertices positions before computing the actual vertices positions
            for path thickness. Note that it is necessary to add the
            glumpy.transforms.Viewport transform at the end of the supplied transform.

        vertex: string
            Vertex shader code

        fragment: string
            Fragment  shader code

        size : string
            'local', 'shared' or 'global'

        orientation : string
            'local', 'shared' or 'global'

        fg_color : string
            'local', 'shared' or 'global'

        bg_color : string
            'local', 'shared' or 'global'

        linewidth : string
            'local', 'shared' or 'global'

        antialias : string
            'local', 'shared' or 'global'
        """

        base_dtype = [ ('position',    (np.float32, 3), '!local', (0,0,0)),
                       ('size',        (np.float32, 1), 'local', 1),
                       ('marker',      (np.float32, 1), 'local', 1),
                       ('orientation', (np.float32, 1), 'local', 0.0),
                       ('fg_color',    (np.float32, 4), 'local', (0,0,0,1)),
                       ('bg_color',    (np.float32, 4), 'local', (1,1,1,1)),
                       ('linewidth',   (np.float32, 1), 'global', 1.0),
                       ('antialias',   (np.float32, 1), 'global', 1.0) ]
        dtype = base_dtype
        if user_dtype:
            dtype.extend(user_dtype)

        if vertex is None:
            vertex = library.get('collections/marker.vert')
        if fragment is None:
            fragment = library.get('collections/marker.frag')

        Collection.__init__(self, dtype=dtype, itype=None, mode=gl.GL_POINTS,
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

        program["marker"] = marker
        program["paint"] = "outline"


    def append(self, P, itemsize = None, **kwargs):
        """
        Append a new set of markers the collection.

        For kwargs argument, n is the number of vertices (local) or the number
        of item (shared)

        Parameters
        ----------

        P : np.array
            Vertices positions of the path(s) to be added

        itemsize: int or None
            Size of an individual path

        size: list, array or float
            Marker size

        fg_color : list, array or 4-tuple
           Path color

        bg_color : list, array or 4-tuple
           Path color

        linewidth : list, array or float
           Path linewidth

        antialias : list, array or float
           Path antialias area
        """

        itemsize  = itemsize or 1
        itemcount = len(P)//itemsize

        V = np.empty(itemcount*itemsize, dtype=self.vtype)

        # Apply default values on vertices
        for name in self.vtype.names:
            if name not in ['collection_index', 'position']:
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
