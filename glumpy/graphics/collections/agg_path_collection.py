# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
"""
Antigrain Geometry Path Collection

This collection provides antialiased and accurate paths with caps and joins. It
is memory hungry (x8) and slow (x.25) so it is to be used sparingly, mainly for
thick paths where quality is critical.
"""
import numpy as np
from glumpy import gl, library
from glumpy.transforms import Position, Viewport
from . collection import Collection



class AggPathCollection(Collection):
    """
    Antigrain Geometry Path Collection

    This collection provides antialiased and accurate paths with caps and
    joins. It is memory hungry (x8) and slow (x.25) so it is to be used
    sparingly, mainly for thick paths where quality is critical.
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
            The viewport to use to rende the collection

        transform: glumpy.Tranforms
            The default vertex shader apply the supplied transform to the
            vertices positions before computing the actual vertices positions
            for path thickness. Note that it is necessary to add the
            glumpy.transforms.Viewport transform at the end of the supplied transform.

        vertex: string
            Vertex shader code

        fragment: string
            Fragment  shader code

        caps : string
            'local', 'shared' or 'global'

        join : string
            'local', 'shared' or 'global'

        color : string
            'local', 'shared' or 'global'

        miter_limit : string
            'local', 'shared' or 'global'

        linewidth : string
            'local', 'shared' or 'global'

        antialias : string
            'local', 'shared' or 'global'
        """

        base_dtype = [ ('p0',         (np.float32, 3), '!local', (0,0,0)),
                       ('p1',         (np.float32, 3), '!local', (0,0,0)),
                       ('p2',         (np.float32, 3), '!local', (0,0,0)),
                       ('p3',         (np.float32, 3), '!local', (0,0,0)),
                       ('uv',         (np.float32, 2), '!local', (0,0)),

                       ('caps',       (np.float32, 2), 'global', (0,0)),
                       ('join',       (np.float32, 1), 'global', 0),
                       ('color',      (np.float32, 4), 'global', (0,0,0,1)),
                       ('miter_limit',(np.float32, 1), 'global', 4),
                       ('linewidth',  (np.float32, 1), 'global', 1),
                       ('antialias',  (np.float32, 1), 'global', 1) ]

        dtype = base_dtype
        if user_dtype:
            dtype.extend(user_dtype)

        if vertex is None:
            vertex = library.get('collections/agg-path.vert')
        if fragment is None:
            fragment = library.get('collections/agg-path.frag')

        Collection.__init__(self, dtype=dtype, itype=np.uint32, mode=gl.GL_TRIANGLES,
                            vertex=vertex, fragment=fragment, **kwargs)

        # Set hooks if necessary
        program = self._programs[0]
        if "transform" in program.hooks:
            if transform is not None:
                program["transform"] = transform
            else:
                program["transform"] = Position() + Viewport()

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

        caps : list, array or 2-tuple
           Path start /end cap

        join : list, array or float
           path segment join

        color : list, array or 4-tuple
           Path color

        miter_limit : list, array or float
           Miter limit for join

        linewidth : list, array or float
           Path linewidth

        antialias : list, array or float
           Path antialias area
        """

        itemsize  = itemsize or len(P)
        itemcount = len(P)//itemsize

        # Computes the adjacency information
        n,p = len(P), P.shape[-1]
        Z = np.tile(P,2).reshape(2*len(P),p)
        V = np.empty(n, dtype=self.vtype)

        V['p0'][1:-1]= Z[0::2][:-2]
        V['p1'][:-1] = Z[1::2][:-1]
        V['p2'][:-1] = Z[1::2][+1:]
        V['p3'][:-2] = Z[0::2][+2:]

        # Apply default values on vertices
        for name in self.vtype.names:
            if name not in ['collection_index', 'p0', 'p1', 'p2', 'p3']:
                V[name] = kwargs.get(name, self._defaults[name])

        # Extract relevant segments only
        V = (V.reshape(n//itemsize, itemsize)[:,:-1])
        if closed:
            V['p0'][:, 0] = V['p2'][:,-1]
            V['p3'][:,-1] = V['p1'][:, 0]
        else:
            V['p0'][:, 0] = V['p1'][:, 0]
            V['p3'][:,-1] = V['p2'][:,-1]
        V = V.ravel()

        # Quadruple each point (we're using 2 triangles / segment)
        # No shared vertices between segment because of joins
        V = np.repeat(V,4,axis=0).reshape((len(V),4))
        V['uv'] = (-1,-1), (-1,+1), (+1,-1), (+1,+1)
        V = V.ravel()

        n = itemsize
        if closed:
            I = np.resize(np.array([0,1,2, 1,2,3], dtype=np.uint32),n*2*3)
            I += np.repeat( 4*np.arange(n, dtype=np.uint32), 6)
            I[-6:] = 4*n-6,4*n-5,0,4*n-5,0,1
        else:
            I = np.resize(np.array([0,1,2, 1,2,3], dtype=np.uint32),(n-1)*2*3)
            I += np.repeat( 4*np.arange(n-1, dtype=np.uint32), 6)
        I = I.ravel()

        # Uniforms
        if self.utype:
            U = np.zeros(itemcount, dtype=self.utype)
            for name in self.utype.names:
                if name not in ["__unused__"]:
                    U[name] = kwargs.get(name, self._defaults[name])
        else:
            U = None

        Collection.append(self, vertices=V, uniforms=U,
                          indices=I, itemsize=itemsize*4-4)


    def draw(self, mode = gl.GL_TRIANGLES):
        """ Draw collection """

        gl.glDepthMask(gl.GL_FALSE)
        Collection.draw(self, mode)
        gl.glDepthMask(gl.GL_TRUE)
