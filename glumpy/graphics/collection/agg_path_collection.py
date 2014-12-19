# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import gl, library
from glumpy.transforms import Position3D, Viewport
from glumpy.graphics.collection.collection import Collection


class AggPathCollection(Collection):
    """
    Antigrain Geometry Path Collection

    This collection provides antialiased and accurate paths with caps and
    joins. It is memory hungry (x8) and slow (x.25) and is to be used
    sparingly, mainly for thick paths where quality is critical.
    """

    def __init__(self, user_dtype=None, transform=None,
                 vertex=None, fragment=None, **kwargs):
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
        if "transform" in self._program._hooks.keys():
            if transform is not None:
                self._program["transform"] = transform
            else:
                self._program["transform"] = Position3D() + Viewport()


    def append(self, P, closed=True, itemsize=None, **kwargs):
        """
        Bake a list of vertices for rendering them as thick line. Each line segment
        must have its own vertices because of antialias (this means no vertex
        sharing between two adjacent line segments).
        """

        itemsize  = itemsize or len(P)
        itemcount = len(P)/itemsize

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
            if name not in ['p0', 'p1', 'p2', 'p3']:
                V[name] = kwargs.get(name, self._defaults[name])

        # Extract relevant segments only
        V = (V.reshape(n/itemsize, itemsize)[:,:-1])
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
            I += np.repeat( 4*np.arange(n), 6)
            I[-6:] = 4*n-6,4*n-5,0,4*n-5,0,1
        else:
            I = np.resize(np.array([0,1,2, 1,2,3], dtype=np.uint32),(n-1)*2*3)
            I += np.repeat( 4*np.arange(n-1), 6)
        I = I.ravel()

        # Uniforms
        if self.utype:
            U = np.zeros(itemcount, dtype=self.utype)
            for name in self.utype.names:
                if name not in ["__unused__"]:
                    U[name] = kwargs.get(name, defaults[name])
        else:
            U = None

        Collection.append(self, vertices=V, uniforms=U,
                          indices=I, itemsize=itemsize*4-4)
