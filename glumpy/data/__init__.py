# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import os
import numpy as np
try:
    from PIL import Image
except:
    Image = None
from glumpy import gloo
from glumpy.log import log


def _get_file(name):
    """ Retrieve a data full path from sub-directories """

    path = os.path.dirname(__file__) or '.'

    filename = os.path.abspath(os.path.join(path,name))
    if os.path.exists(filename):
        return filename

    for d in os.listdir(path):
        fullpath = os.path.abspath(os.path.join(path,d))
        if os.path.isdir(fullpath):
            filename = os.path.abspath(os.path.join(fullpath,name))
            if os.path.exists(filename):
                return filename
    return None


def objload(filename) :
    V = [] #vertex
    T = [] #texcoords
    N = [] #normals
    F = [] #face indexies
    for line in open(filename):
        if line[0] == '#':
            continue
        line = line.strip().split(' ')
        if line[0] == 'v':     #vertex
            V.append(map(float,line[1:]))
        elif line[0] == 'vt' : # tex-coord
            T.append(map(float,line[1:]))
        elif line[0] == 'vn' : # normal vector
            N.append(map(float,line[1:]))
        elif line[0] == 'f' :  # face
            face = line[1:]
            if len(face) != 3 :
                raise Exception('not a triangle')
            for i in range(0, len(face)) :
                face[i] = face[i].split('/')
                for j in range(0, len(face[i])):
                    face[i][j] = int(face[i][j]) - 1
            F.append(face)

    hashes = []
    indices = []
    vertices = []
    for face in F:
        for i in range(3):
            h = hash(tuple(face[i]))
            if h in hashes:
                j = hashes.index(h)
            else:
                j = len(hashes)
                vertices.append( (V[face[i][0]],
                                  T[face[i][1]],
                                  N[face[i][2]]) )
                hashes.append(h)
            indices.append(j)
    vtype = [('position', np.float32, 3),
             ('texcoord', np.float32, 2),
             ('normal',   np.float32, 3)]
    itype = np.uint32

    vertices = np.array(vertices, dtype=vtype).view(gloo.VertexBuffer)
    indices = np.array(indices, dtype=itype).view(gloo.IndexBuffer)
    return vertices, indices


def checkerboard(grid_num=16, grid_size=24):
    row_even = grid_num / 2 * [0, 1]
    row_odd = grid_num / 2 * [1, 0]
    Z = np.row_stack(grid_num / 2 * (row_even, row_odd)).astype(np.uint8)
    return 255 * Z.repeat(grid_size, axis=0).repeat(grid_size, axis=1)


def get(name):
    """ Retrieve data content from a name """

    filename = _get_file(name)
    extension = os.path.basename(name).split('.')[-1]

    if extension == 'npy':
        return np.load(filename)
    elif extension == 'obj':
        return objload(filename)
    elif extension in ('png', 'jpg', 'jpeg', 'tif', 'tiff', 'tga'):
        if Image is not None:
            return np.array(Image.open(filename))
        else:
            log.warning("PIL/Pillow not installed, cannot load image")
            return checkerboard(16,32)

    log.warning("Data not found(%s)" % name)
    return None
