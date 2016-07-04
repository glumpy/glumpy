# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import os
from glumpy.ext.six.moves.urllib import request
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
        response = request.urlopen(remote)
    except:
        log.warning('Data not available on remote server')
        return None
    # Fetch symlink data (font location)
    symlink = response.read().decode()

    remote = os.path.join(server, symlink)
    response = request.urlopen(remote)

    # Fetch data
    size = response.headers['Content-Length'].strip()
    log.info('Fetching data (%s bytes) to "%s"' % (size, local_file))
    with open(local_file, 'wb') as fp:
        fp.write(response.read())
    return local_file



def objload(filename, rescale=True):
    """ """
    
    V = [] # vertex
    T = [] # texcoords
    N = [] # normals
    F   = [] # face indices
    F_V = [] # face indices
    F_T = [] # face indices
    F_N = [] # face indices
    
    for lineno,line in enumerate(open(filename)):
        if line[0] == '#':
            continue
        values = line.strip().split(' ')
        code = values[0]
        values = values[1:]
        # vertex (v)
        if code == 'v':
            V.append([float(x) for x in values])
        # tex-coord (vt)
        elif code == 'vt' :
            T.append([float(x) for x in values])
        # normal (n)
        elif code == 'vn' :
            N.append([float(x) for x in values])
        # face (f)
        elif code == 'f' :
            if len(values) != 3:
                raise ValueError('not a triangle at line' % lineno)
            for v in values:
                for j,index in enumerate(v.split('/')):
                    if len(index):
                        if   j==0: F_V.append(int(index)-1)
                        elif j==1: F_T.append(int(index)-1)
                        elif j==2: F_N.append(int(index)-1)

    # Building the vertices
    V = np.array(V)
    F_V = np.array(F_V)
    vtype = [('position', np.float32, 3)]
    
    if len(T):
        T = np.array(T)
        F_T = np.array(F_T)
        vtype.append(('texcoord', np.float32, 2))
    if len(N):
        N = np.array(N)
        F_N = np.array(F_N)
        vtype.append(('normal', np.float32, 3))
        
    vertices = np.empty(len(F_V),vtype)
    vertices["position"] = V[F_V,:3]
    if len(T):
        vertices["texcoord"] = T[F_T,:2]
    if len(N):
        vertices["normal"] = N[F_N]
    vertices = vertices.view(gloo.VertexBuffer)

    if rescale:
        # Centering and scaling to fit the unit box
        xmin,xmax = vertices["position"][:,0].min(), vertices["position"][:,0].max()
        ymin,ymax = vertices["position"][:,1].min(), vertices["position"][:,1].max()
        zmin,zmax = vertices["position"][:,2].min(), vertices["position"][:,2].max()
        vertices["position"][:,0] -= (xmax+xmin)/2.0
        vertices["position"][:,1] -= (ymax+ymin)/2.0
        vertices["position"][:,2] -= (zmax+zmin)/2.0
        scale = max(max(xmax-xmin,ymax-ymin), zmax-zmin) / 2.0
        vertices["position"] /= scale
    
        # xmin,xmax = vertices["position"][:,0].min(), vertices["position"][:,0].max()
        # ymin,ymax = vertices["position"][:,1].min(), vertices["position"][:,1].max()
        # zmin,zmax = vertices["position"][:,2].min(), vertices["position"][:,2].max()
        # print("xmin: %g, xmax: %g" % (xmin,xmax))
        # print("ymin: %g, xmax: %g" % (ymin,ymax))
        # print("zmin: %g, zmax: %g" % (zmin,zmax))
    
    itype = np.uint32
    indices = np.arange(len(vertices), dtype=np.uint32)
    indices = indices.view(gloo.IndexBuffer)
    return vertices, indices


def checkerboard(grid_num=8, grid_size=32):
    row_even = grid_num // 2 * [0, 1]
    row_odd = grid_num // 2 * [1, 0]
    Z = np.row_stack(grid_num // 2 * (row_even, row_odd)).astype(np.uint8)
    return 255 * Z.repeat(grid_size, axis=0).repeat(grid_size, axis=1)


def get(name, *args, **kwargs): #, depth=0):
    """ Retrieve data content from a name """

    if name == "checkerboard":
        return checkerboard(8,16)

    filename = _fetch_file(name)
    return load(filename, *args, **kwargs)


def load(filename, *args, **kwargs):
    """ Load data content from a filename """
    
    extension = os.path.basename(filename).split('.')[-1]

    if extension == 'npy':
        return np.load(filename, *args, **kwargs)
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
        return objload(filename, *args, **kwargs)
    elif extension in ['svg', 'json', 'csv', 'tsv']:
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
