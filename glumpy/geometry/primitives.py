# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import gloo, data


def plane(size=1.0, n=2):
    """
    Plane centered at origin, lying on the XY-plane

    Parameters
    ----------
    size : float
       plane length size

    n : int
        Tesselation level
    """

    n = max(2,n)

    T = np.linspace(0,1,n,endpoint=True)
    X,Y = np.meshgrid(T-0.5,T-0.5)
    X = X.ravel()*size
    Y = Y.ravel()*size
    U,V = np.meshgrid(T,T)
    U = U.ravel()
    V = V.ravel()

    I = (np.arange((n-1)*(n),dtype=np.uint32).reshape(n-1,n))[:,:-1].T
    I = np.repeat(I.ravel(),6).reshape(n-1,n-1,6)
    I[:,:] += np.array([0,1,n+1, 0,n+1,n], dtype=np.uint32)

    vtype = [('position', np.float32, 3),
             ('texcoord', np.float32, 2),
             ('normal',   np.float32, 3)]
    itype = np.uint32

    vertices = np.zeros((6,n*n), dtype=vtype)
    vertices["texcoord"][...,0] = U
    vertices["texcoord"][...,1] = V
    vertices["position"][0,:,0] = X
    vertices["position"][0,:,1] = Y
    vertices["position"][0,:,2] = 0
    vertices["normal"][0] = 0,0,1

    vertices = vertices.ravel()
    indices = np.array(I, dtype=itype).ravel()
    return vertices.view(gloo.VertexBuffer), indices.view(gloo.IndexBuffer)



def cube(size=1.0, n=2):
    """
    Cube centered at origin

    Parameters
    ----------
    size : float
       cube length size

    n : int
        Tesselation level
    """

    n = max(2,n)

    T = np.linspace(0,1,n,endpoint=True)
    X,Y = np.meshgrid(T-0.5,T-0.5)
    X = X.ravel()*size
    Y = Y.ravel()*size
    Z = np.ones_like(X)*0.5*size
    U,V = np.meshgrid(T,T)
    U = U.ravel()
    V = V.ravel()

    I = (np.arange((n-1)*(n),dtype=np.uint32).reshape(n-1,n))[:,:-1].T
    I = np.repeat(I.ravel(),6).reshape(n-1,n-1,6)
    I[:,:] += np.array([0,1,n+1, 0,n+1,n], dtype=np.uint32)

    vtype = [('position', np.float32, 3),
             ('texcoord', np.float32, 2),
             ('normal',   np.float32, 3)]
    itype = np.uint32
    vertices = np.zeros((6,n*n), dtype=vtype)

    vertices["texcoord"][...,0] = U
    vertices["texcoord"][...,1] = V

    # Top
    vertices["position"][0,:,0] = X
    vertices["position"][0,:,1] = Y
    vertices["position"][0,:,2] = Z
    vertices["normal"][0] = 0,0,1

    # Bottom
    vertices["position"][1,:,0] = X
    vertices["position"][1,:,1] = Y
    vertices["position"][1,:,2] = -Z
    vertices["normal"][1] = 0,0,-1

    # Front
    vertices["position"][2,:,0] = Z
    vertices["position"][2,:,1] = X
    vertices["position"][2,:,2] = Y
    vertices["normal"][2] = 1,0,0

    # Back
    vertices["position"][3,:,0] = -Z
    vertices["position"][3,:,1] = X
    vertices["position"][3,:,2] = Y
    vertices["normal"][3] = -1,0,0

    # Left
    vertices["position"][4,:,0] = X
    vertices["position"][4,:,1] = Z
    vertices["position"][4,:,2] = Y
    vertices["normal"][4] = 0,1,0

    # Right
    vertices["position"][5,:,0] = X
    vertices["position"][5,:,1] = -Z
    vertices["position"][5,:,2] = Y
    vertices["normal"][5] = 0,-1,0

    I = I.ravel()
    indices = np.zeros((6,len(I)), dtype=itype)
    indices[:] = I
    indices += (np.arange(6,dtype=np.uint32)*n*n).reshape(6,1)

    vertices = vertices.ravel()
    indices = indices.ravel()
    return vertices.view(gloo.VertexBuffer), indices.view(gloo.IndexBuffer)



def tube(top_radius=1.0, base_radius=1.0, height=2.0, slices=32, caps=(True,True)):
    """
    Z-axis aligned tube centered at origin.

    Parameters
    ----------
    top_radius : float
        The radius at the top of the cylinder
    base_radius : float
        The radius at the base of the cylinder
    height : float
        The height of the cylinder
    slices : float
        The number of subdivisions around the Z axis.
    caps : bool, bool
        Whether to add caps at top and bottom
    """

    vtype = [('position', np.float32, 3),
             ('texcoord', np.float32, 2),
             ('normal',   np.float32, 3)]
    itype = np.uint32

    if top_radius <= 0.0:
        caps[0] = False
    if base_radius <= 0.0:
        caps[1] = False

    theta  = np.linspace(0,2*np.pi, slices+1, endpoint=True)
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)

    n_side = slices+1
    n_cap  = slices+1
    n = 2*n_side + caps[0]*n_cap + caps[1]*n_cap

    i0 = 0           # Start index of base side
    i1 = i0 + n_side # Start index of top side

    vertices = np.zeros(n, dtype=vtype)
    sides    = vertices[:2*n_side]
    topside  = sides[:+n_side]
    baseside = sides[-n_side:]
    if caps[0] and caps[1]:
        C = vertices[-2*n_cap:]
        topcap   = C[:+n_cap]
        basecap  = C[-n_cap:]
        i2 = i1 + n_side # Start index of top cap
        i3 = i2 + n_cap  # Start index of base cap
    elif caps[0]:
        topcap = vertices[-n_cap:]
        basecap = None
        i2 = i1 + n_side # Start index of top cap
        i3 = None
    elif caps[1]:
        topcap = None
        basecap = vertices[-n_cap:]
        i2 = None
        i3 = i1 + n_side # Start index of top cap

    r = (top_radius-base_radius)
    hypothenus = np.sqrt(r*r + height*height)

    topside["position"][:,0] = cos_theta * top_radius
    topside["position"][:,1] = sin_theta * top_radius
    topside["position"][:,2] = +height/2.0
    topside["texcoord"][:,0] = np.linspace(0,1,slices+1,endpoint=True)
    topside["texcoord"][:,1] = 0
    topside["normal"][:,0] = cos_theta * height/hypothenus
    topside["normal"][:,1] = sin_theta * height/hypothenus
    topside["normal"][:,2] = -(top_radius-base_radius)/hypothenus


    baseside["position"][:,0] = cos_theta * base_radius
    baseside["position"][:,1] = sin_theta * base_radius
    baseside["position"][:,2] = -height/2.0
    baseside["texcoord"][:,0] = np.linspace(0,1,slices+1,endpoint=True)
    baseside["texcoord"][:,1] = 1
    baseside["normal"][:,0] = cos_theta * height/hypothenus
    baseside["normal"][:,1] = sin_theta * height/hypothenus
    baseside["normal"][:,2] = -(top_radius-base_radius)/hypothenus

    if caps[0]:
        topcap["position"][1:] = topside["position"][:-1]
        topcap["position"][0]  = 0, 0, +height/2.0
        topcap["texcoord"][1:,0] = (1+cos_theta[:-1])/2
        topcap["texcoord"][1:,1] = (1+sin_theta[:-1])/2
        topcap["texcoord"][0]  = 0.5, 0.5
        topcap["normal"]  = 0,0,+1
    if caps[1]:
        basecap["position"][1:] = baseside["position"][:-1]
        basecap["position"][0]  = 0, 0, -height/2.0
        basecap["texcoord"][1:,0] = (1+cos_theta[:-1])/2
        basecap["texcoord"][1:,1] = (1+sin_theta[:-1])/2
        basecap["texcoord"][0]  = 0.5, 0.5
        basecap["normal"]  = 0,0,-1

    indices = []
    # side triangles
    for i in range(slices):
        indices.extend([i0+i, i0+i+1, i1+i  ])
        indices.extend([i1+i, i1+i+1, i0+i+1])

    # caps triangles
    for i in range(slices+1):
        if caps[0]:
            indices.extend([i2,i2+1+i%slices,i2+1+(i+1)%slices])
        if caps[1]:
            indices.extend([i3,i3+1+i%slices,i3+1+(i+1)%slices])

    indices = np.array(indices, dtype=itype)
    return vertices.view(gloo.VertexBuffer), indices.view(gloo.IndexBuffer)



def cylinder(radius=0.5, height=2.0, slices=32, caps=(True,True)):
    """
    Z-axis aligned cylinder centered a origin.

    Parameters
    ----------
    radius : float
        The radius of the cylinder
    height : float
        The height of the cylinder
    slices : float
        The number of subdivisions around the Z axis.
    caps : bool, bool
        Whether to add caps at top and bottom
    """

    return tube(radius, radius, height, slices, caps)


def cone(radius=1.0, height=1.0, slices=32, cap=True):
    """
    Z-axis aligned cone.

    The base of the cone is placed at z=0, and the top at z=+height. The
    cone is subdivided around the Z axis into slices.

    Parameters
    ----------
    radius : float
        The radius of the base of the cone.
    height : float
        The height of the cone.
    slices : float
        The number of subdivisions around the Z axis.
    cap : bool
        Whether to add cap at base
    """
    vertices, indices = tube(0, radius, height, slices, caps=[False,cap])
    vertices["position"] += 0,0, height/2.0
    return vertices, indices


def pyramid(radius=1.0, height=1.0, cap=True):
    """
    Z-axis aligned pyramid.

    The base of the cone is placed at z=0, and the top at z=+height. The
    cone is subdivided around the Z axis into slices.

    Parameters
    ----------
    radius : float
        The radius of the base of the cone.
    height : float
        The height of the cone.
    slices : float
        The number of subdivisions around the Z axis.
    cap : bool
        Whether to add cap at base
    """
    vertices, indices = tube(0, radius, height, 4, caps=[False,cap])
    vertices["position"] += 0,0, height/2.0
    return vertices, indices


def torus(inner_radius=0.25, outer_radius=1.0, sides=32, rings=48):
    """
    Z-axis aligned torus (doughnut) centered at origin.

    Parameters
    ----------
    inner_radius : float
        Inner radius of the torus.
    outer_radius : float
        Outer radius of the torus.
    sides : int
        Number of sides for each radial section.
    rings : int
        Number of radial divisions for the torus.
    """

    vtype = [('position', np.float32, 3),
             ('texcoord', np.float32, 2),
             ('normal',   np.float32, 3)]
    itype = np.uint32
    sides += 1
    rings += 1
    n = rings * sides

    vertices = np.zeros(n, dtype=vtype)
    theta1 = np.tile  (np.linspace(0, 2 * np.pi, sides, endpoint=True), rings)
    theta2 = np.repeat(np.linspace(0, 2 * np.pi, rings, endpoint=True), sides)
    C = inner_radius*np.cos(theta1) - outer_radius

    vertices["position"][:,0] = C*np.cos(theta2)
    vertices["position"][:,1] = C*np.sin(theta2)
    vertices["position"][:,2] = inner_radius*np.sin(theta1)
    vertices["normal"][:,0] = (C+outer_radius)*np.cos(theta2)
    vertices["normal"][:,1] = (C+outer_radius)*np.sin(theta2)
    vertices["normal"][:,2] = vertices["position"][:,2]
    vertices["texcoord"][:,0] = np.tile(np.linspace(0,1,sides,endpoint=True),rings)
    vertices["texcoord"][:,1] = np.repeat(np.linspace(0,1,rings,endpoint=True),sides)

    indices = []
    for i in range(rings-1):
        for j in range(sides-1):
            indices.append(i*(sides) + j        )
            indices.append(i*(sides) + j+1      )
            indices.append(i*(sides) + j+sides+1)
            indices.append(i*(sides) + j+sides  )
            indices.append(i*(sides) + j+sides+1)
            indices.append(i*(sides) + j        )

    indices = np.array(indices, dtype=itype)
    return vertices.view(gloo.VertexBuffer), indices.view(gloo.IndexBuffer)


def sphere(radius=1.0, slices=32, stacks=32):
    """
    Sphere centered at origin.

    The sphere is subdivided around the Z axis into slices and along the Z axis
    into stacks.

    Parameters
    ----------
    radius : float
        The radius of the sphere.
    slices : float
        The number of subdivisions around the Z axis (similar to lines of longitude).
    stacks : float
        The number of subdivisions along the Z axis (similar to lines of latitude).
    """

    vtype = [('position', np.float32, 3),
             ('texcoord', np.float32, 2),
             ('normal',   np.float32, 3)]
    itype = np.uint32
    slices += 1
    stacks += 1
    n = slices*stacks

    vertices = np.zeros(n, dtype=vtype)
    theta1 = np.repeat(np.linspace(0,     np.pi, stacks, endpoint=True), slices)
    theta2 = np.tile  (np.linspace(0, 2 * np.pi, slices, endpoint=True), stacks)

    vertices["position"][:,1] = np.sin(theta1) * np.cos(theta2) * radius
    vertices["position"][:,2] =                  np.cos(theta1) * radius
    vertices["position"][:,0] = np.sin(theta1) * np.sin(theta2) * radius
    vertices["normal"] = vertices["position"]
    vertices["texcoord"][:,0] = np.tile(np.linspace(0, 1, slices, endpoint=True), stacks)
    vertices["texcoord"][:,1] = np.repeat(np.linspace(1, 0, stacks, endpoint=True), slices)

    indices = []
    for i in range(stacks-1):
        for j in range(slices-1):
            indices.append(i*(slices) + j        )
            indices.append(i*(slices) + j+1      )
            indices.append(i*(slices) + j+slices+1)
            indices.append(i*(slices) + j+slices  )
            indices.append(i*(slices) + j+slices+1)
            indices.append(i*(slices) + j        )

    indices = np.array(indices, dtype=itype)
    return vertices.view(gloo.VertexBuffer), indices.view(gloo.IndexBuffer)


def cubesphere(radius=1.0, n=32):
    """
    Cubesphere (cube warped into sphere) centered at origin.

    Parameters
    ----------
    radius : float
        The radius of the sphere.
    n : int
        Tesselation level
    """

    vertices, indices = cube(1.0,n)
    L = np.sqrt((vertices["position"]**2).sum(axis=1))
    vertices["position"] /= L.reshape(len(vertices),1)/radius
    vertices["normal"] = vertices["position"]
    return vertices, indices




def teapot(size=1.0):
    """
    Z-axis aligned Utah teapot

    Parameters
    ----------

    size : float
        Relative size of the teapot.
    """

    vertices, indices = data.get("teapot.obj")
    xmin = vertices["position"][:,0].min()
    xmax = vertices["position"][:,0].max()
    ymin = vertices["position"][:,1].min()
    ymax = vertices["position"][:,1].max()
    zmin = vertices["position"][:,2].min()
    zmax = vertices["position"][:,2].max()

    # Centering
    vertices["position"][:,0] -= xmin + (xmax-xmin)/2
    vertices["position"][:,1] -= ymin + (ymax-ymin)/2
    vertices["position"][:,2] -= zmin + (zmax-zmin)/2

    # Rotation to align on Z-axis
    X = vertices["position"][:,0].copy()
    Y = vertices["position"][:,1].copy()
    Z = vertices["position"][:,2].copy()
    NX = vertices["normal"][:,0].copy()
    NY = vertices["normal"][:,1].copy()
    NZ = vertices["normal"][:,2].copy()
    vertices["position"][:,0] = X
    vertices["position"][:,1] = Z
    vertices["position"][:,2] = Y
    vertices["normal"][:,0] = NX
    vertices["normal"][:,1] = NZ
    vertices["normal"][:,2] = NY

    # Scaling according to height
    vertices["position"] *= 2.0*size/(zmax-zmin)

    return vertices, indices
