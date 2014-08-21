# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import numpy as np

def cross(X, Y):
    """
    Compute cross product between list of 3D vectors.

    Much faster than np.cross() when the number of cross products
    becomes large (>500). This is because np.cross() methods become
    less memory efficient at this stage.

    Parameters
    ----------
    x : array
        Input array 1
    y : array
        Input array 2
    """

    if max([x.shape[0], y.shape[0]]) >= 500:
        return np.c_[x[:,1] * y[:,2] - x[:,2] * y[:,1],
                     x[:,2] * y[:,0] - x[:,0] * y[:,2],
                     x[:,0] * y[:,1] - x[:,1] * y[:,0]]
    else:
        return np.cross(x,y)


def normals(vertices, indices):
    """
    Compute normals over a triangulated surface

    Parameters
    ----------

    vertices : ndarray
        triangles vertices

    indices : ndarray
        triangles indices
    """

    # Triangles normals
    v1 = vertices[indices[:,0]]
    v2 = vertices[indices[:,1]]
    v3 = vertices[indices[:,2]]
    N = cross(v2-v1, v3-v1)
    L = np.sqrt(np.sum(N*N,axis=1))
    L[L==0] = 1.0  # prevent divide-by-zero
    N /= L[:, np.newaxis]

    # Shared normals
    normals = np.zeros((len(vertices), 3))
    for verts in indices.T:
        for i in xrange(3):
            normals[:,i] += np.bincount(verts, N[:,i], minlength=len(vertices))
    L = np.sqrt(np.sum(normals*normals, axis=1))
    L[L== 0] = 1.0
    normals /= L[:,np.newaxis]

    return normals
