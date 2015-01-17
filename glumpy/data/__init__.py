# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import os
import urllib2
import numpy as np
try:
    from PIL import Image
except:
    Image = None
from glumpy import gloo
from glumpy.log import log


def _fetch_file(filename):
    """
    Fetch a font file from a remote data server

    Available servers:

      * https://github.com/glumpy/glumpy-font/raw/master/Fonts
      * https://github.com/glumpy/glumpy-data/raw/master/Data
    """

    local_directory = os.path.dirname(__file__) or '.'
    local_file = os.path.join(local_directory, filename)

    if os.path.isfile(local_file):
        return local_file

    extension = os.path.basename(filename).split('.')[-1]

    # Font server
    if extension in ['ttf', 'otf']:
        server = "https://github.com/glumpy/glumpy-font/raw/master/Fonts"
    # Data server
    else:
        server = "https://github.com/glumpy/glumpy-data/raw/master/Data"

    filename = os.path.basename(filename)
    remote = os.path.join(server, filename)

    # Build url request
    log.info('Requesting "%s" from remote server' % filename)
    try:
        response = urllib2.urlopen(remote)
    except:
        log.warning('Data not available on remote server')
        return None
    # Fetch symlink data (font location)
    symlink = response.read()

    remote = os.path.join(server, symlink)
    response = urllib2.urlopen(remote)

    # Fetch data
    size = response.headers['Content-Length'].strip()
    log.info('Fetching data (%s bytes) to "%s"' % (size, local_file))
    with open(local_file, 'wb') as fp:
        fp.write(response.read())
    return local_file



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


def checkerboard(grid_num=8, grid_size=32):
    row_even = grid_num / 2 * [0, 1]
    row_odd = grid_num / 2 * [1, 0]
    Z = np.row_stack(grid_num / 2 * (row_even, row_odd)).astype(np.uint8)
    return 255 * Z.repeat(grid_size, axis=0).repeat(grid_size, axis=1)


def get(name, depth=0):
    """ Retrieve data content from a name """

    if name == "checkerboard":
        return checkerboard(8,16)

    extension = os.path.basename(name).split('.')[-1]
    filename = _fetch_file(name)
    if extension == 'npy':
        return np.load(filename)
    elif extension in ['ttf', 'otf']:
        if filename is not None:
            return filename
        if depth == 0:
            log.warning("Falling back to default font")
            return get("SourceSansPro-Regular.otf", 1)
        else:
            log.critical("Default font not available")
            raise RuntimeError
    elif extension == 'obj':
        return objload(filename)
    elif extension == 'svg':
        return filename
    elif extension in ('png', 'jpg', 'jpeg', 'tif', 'tiff', 'tga'):
        if Image is not None:
            if filename is not None:
                return np.array(Image.open(filename))
            log.warning("File not found")
            return checkerboard(16,32)
        else:
            log.warning("PIL/Pillow not installed, cannot load image")
            return checkerboard(16,32)

    log.warning("Data not found (%s)" % name)
    raise RuntimeError
    return None
