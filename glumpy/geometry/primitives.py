# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import gloo


def cube(size=2.0):
    """
    Cube centered at origin

    Parameters
    ----------
    size : float
       cube length size
    """

    vtype = [('position', np.float32, 3),
             ('texcoord', np.float32, 2),
             ('normal',   np.float32, 3)]
    itype = np.uint32

    # Vertices positions
    p = np.array([[1, 1, 1], [-1, 1, 1], [-1, -1, 1], [1, -1, 1],
                  [1, -1, -1], [1, 1, -1], [-1, 1, -1], [-1, -1, -1]], dtype=np.float32)
    p *= size/2.0, size/2.0, size/2.0


    # Face Normals
    n = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0],
                  [-1, 0, 1], [0, -1, 0], [0, 0, -1]])
    # Texture coords
    t = np.array([[0, 0], [0, 1], [1, 1], [1, 0]])

    faces_p = [0, 1, 2, 3,
               0, 3, 4, 5,
               0, 5, 6, 1,
               1, 6, 7, 2,
               7, 4, 3, 2,
               4, 7, 6, 5]
    faces_n = [0, 0, 0, 0,
               1, 1, 1, 1,
               2, 2, 2, 2,
               3, 3, 3, 3,
               4, 4, 4, 4,
               5, 5, 5, 5]
    faces_t = [0, 1, 2, 3,
               0, 1, 2, 3,
               0, 1, 2, 3,
               3, 2, 1, 0,
               0, 1, 2, 3,
               0, 1, 2, 3]

    vertices = np.zeros(24, vtype)
    vertices['position'] = p[faces_p]
    vertices['normal'] = n[faces_n]
    vertices['texcoord'] = t[faces_t]
    indices = np.resize(np.array([0,1,2,0,2,3], dtype=itype), 6*(2*3))
    indices+= np.repeat(4 * np.arange(6, dtype=itype), 6)

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



def cylinder(radius=1.0, height=2.0, slices=32, caps=(True,True)):
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
    vertices, incides = tube(0, radius, height, 4, caps=[False,cap])
    vertices["position"] += 0,0, height/2.0
    return vertices, indices



def sphere(radius=1.0, slices=24, stacks=24):
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
    pass



def icosphere(radius=1.0, slices=24, stacks=24):
    """
    Icosphere (without poles) centered at origin.

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
    pass



def torus(inner_radius=0.2, outer_radius=1.0, nsides=24, rings=24):
    """
    Z-axis aligned torus (doughnut) centered at origin.

    Parameters
    ----------
    inner_radius : float
        Inner radius of the torus.
    outer_radius : float
        Outer radius of the torus.
    nsides : int
        Number of sides for each radial section.
    rings : int
        Number of radial divisions for the torus.
    """
    pass




def teapot(size=1.0):
    """
    Z-axis aligned Utah teapot

    Parameters
    ----------

    size : float
        Relative size of the teapot.
    """
    pass
