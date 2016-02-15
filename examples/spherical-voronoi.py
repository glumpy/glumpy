# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
import numpy.matlib
import scipy.spatial
import itertools
from glumpy import app, gl
from glumpy.graphics.collections import TriangleCollection, PathCollection
from glumpy.transforms import Position, Trackball

# -----------------------------------------------------------------------------
# Copyright (C)  Tyler Reddy, Ross Hemsley, Edd Edmondson,
#                Nikolai Nowaczyk, Joe Pitt-Francis, 2015.
#
# Distributed under the same BSD license as Scipy.
# -----------------------------------------------------------------------------
# This will soon appear in scipy.spatial, until then the code has been inserted
# See: https://github.com/scipy/scipy/pull/5232
# -----------------------------------------------------------------------------
def calc_circumcenters(tetrahedrons):
    num = tetrahedrons.shape[0]
    a = np.concatenate((tetrahedrons, np.ones((num, 4, 1))), axis=2)
    sums = np.sum(tetrahedrons ** 2, axis=2)
    d = np.concatenate((sums[:, :, np.newaxis], a), axis=2)
    dx = np.delete(d, 1, axis=2)
    dy = np.delete(d, 2, axis=2)
    dz = np.delete(d, 3, axis=2)
    dx = np.linalg.det(dx)
    dy = -np.linalg.det(dy)
    dz = np.linalg.det(dz)
    a = np.linalg.det(a)
    nominator = np.vstack((dx, dy, dz))
    denominator = 2*a
    return (nominator / denominator).T

def project_to_sphere(points, center, radius):
    lengths = scipy.spatial.distance.cdist(points, np.array([center]))
    return (points - center) / lengths * radius + center

class SphericalVoronoi:
    def __init__(self, points, radius=None, center=None):
        self.points = points
        if np.any(center):
            self.center = center
        else:
            self.center = np.zeros(3)
        if radius:
            self.radius = radius
        else:
            self.radius = 1
        self.vertices = None
        self.regions = None
        self._tri = None
        self._calc_vertices_regions()

    def _calc_vertices_regions(self):
        self._tri = scipy.spatial.ConvexHull(self.points)
        tetrahedrons = self._tri.points[self._tri.simplices]
        tetrahedrons = np.insert(
            tetrahedrons,
            3,
            np.array([self.center]),
            axis=1
        )
        circumcenters = calc_circumcenters(tetrahedrons)
        self.vertices = project_to_sphere(
            circumcenters,
            self.center,
            self.radius )
        generator_indices = np.arange(self.points.shape[0])
        filter_tuple = np.where((np.expand_dims(self._tri.simplices,
                                -1) == generator_indices).any(axis=1))
        list_tuples_associations = zip(filter_tuple[1],
                                       filter_tuple[0])
        list_tuples_associations = sorted(list_tuples_associations,
                                          key=lambda t: t[0])
        groups = []
        for k, g in itertools.groupby(list_tuples_associations,
                                      lambda t: t[0]):
            groups.append([element[1] for element in list(g)])
        self.regions = groups

    def sort_vertices_of_regions(self):
        for n in range(0, len(self.regions)):
            remaining = self.regions[n][:]
            sorted_vertices = []
            current_simplex = remaining[0]
            current_vertex = [k for k in self._tri.simplices[current_simplex]
                              if k != n][0]
            remaining.remove(current_simplex)
            sorted_vertices.append(current_simplex)
            while remaining:
                current_simplex = [
                    s for s in remaining
                    if current_vertex in self._tri.simplices[s]
                    ][0]
                current_vertex = [
                    s for s in self._tri.simplices[current_simplex]
                    if s != n and s != current_vertex
                    ][0]
                remaining.remove(current_simplex)
                sorted_vertices.append(current_simplex)
            self.regions[n] = sorted_vertices
# -----------------------------------------------------------------------------
            
window = app.Window(1200, 1200, color=(1,1,1,1))

@window.event
def on_draw(dt):
    window.clear()

    # Cells
    gl.glDisable(gl.GL_BLEND)
    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glEnable(gl.GL_POLYGON_OFFSET_FILL)
    cells.draw()

    # Cell outlines
    gl.glDisable(gl.GL_POLYGON_OFFSET_FILL)
    gl.glEnable(gl.GL_BLEND)
    gl.glDepthMask(gl.GL_FALSE)
    outlines.draw()
    gl.glDepthMask(gl.GL_TRUE)

@window.event
def on_init():
    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glPolygonOffset(1, 1)
    gl.glEnable(gl.GL_LINE_SMOOTH)
    gl.glLineWidth(0.75)

transform = Trackball(Position())
cells     = TriangleCollection("raw", transform=transform, color='shared')
outlines  = PathCollection("raw", transform=transform, color='shared')

# Random points
n = 2000
points = np.random.normal(size=(n, 3)) 
points /= np.linalg.norm(points, axis=1)[:, np.newaxis]

# Voronoi cells
sv = SphericalVoronoi(points, 2, (0,0,0))
sv.sort_vertices_of_regions()

for region in sv.regions:
    z = np.random.uniform(0,1)

    V = (1.0+0.1*z) * sv.vertices[region]
    color = (.75+.25*z,.25+.75*z,.25+.75*z,1)

    I = np.zeros((len(V)-2,3))
    I[:,1] = 1 + np.arange(len(I))
    I[:,2] = 1 + I[:,1]
    cells.append(V, I.ravel(), color=color)
    outlines.append(V, color=(0,0,0,1), closed=True)

    V_ = []
    for v1,v2 in zip(V[:-1],V[1:]):
        V_.extend(((0,0,0),v1,v2))
    V_.extend(((0,0,0), V[-1], V[0]))
    
    V_ = np.array(V_)
    I = np.arange(len(V_))
    cells.append(V_, I, color=color)
    outlines.append(V_, color=(0,0,0,1), closed=True)
    

window.attach(outlines["transform"])
window.attach(outlines["viewport"])
app.run()
