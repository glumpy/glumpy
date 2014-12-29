#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import sys
import numpy as np
from glumpy import app, collections
from glumpy.transforms import Position3D, OrthographicProjection, Viewport

from scipy.spatial import cKDTree
from scipy.spatial.distance import cdist


def graph(links = [(0,1), (1,2), (2,3), (3,0), (0,2), (1,3),
                   (3,4), (4,5), (5,6), (6,7),
                   (7,8), (8,9), (9,10), (10,7), (8,10), (7,9) ]):

    ntype = np.dtype( [('position', 'f4', 3),
                       ('previous', 'f4', 3),
                       ('weight',   'f4', 1),
                       ('charge',   'f4', 1),
                       ('fixed',    'b',  1)] )
    ltype = np.dtype( [('source',   'i4', 1),
                       ('target',   'i4', 1),
                       ('strength', 'f4', 1),
                       ('distance', 'f4', 1)] )
    L = np.array(links).reshape(len(links),2)
    L -= L.min()
    n = L.max()+1
    nodes = np.zeros(n, ntype)
    nodes['position'][:,:2] = np.random.uniform(400-32, 400+32, (n,2))
    nodes['previous'] = nodes['position']
    nodes['fixed'] = False
    nodes['weight'] = 1
    nodes['charge'] = 1

    l = len(L)
    links = np.zeros( n+l, ltype)
    links[:n]['source'] = np.arange(0,n)
    links[:n]['target'] = np.arange(0,n)
    links[n:]['source'] = L[:,0]
    links[n:]['target'] = L[:,1]
    links['distance'] = 40
    links['strength'] = 5

    I = np.argwhere(links['source']==links['target'])
    links['distance'][I] = links['strength'][I] = 0

    return nodes,links



def relaxation(nodes, links):
    """ Gauss-Seidel relaxation for links """

    sources_idx = links['source']
    targets_idx = links['target']
    sources   = nodes[sources_idx]
    targets   = nodes[targets_idx]
    distances = links['distance']
    strengths = links['strength']

    D = (targets['position'] - sources['position'])
    L = np.sqrt((D*D).sum(axis=1))

    # This avoid to test L != 0 (I = np.where(L>0))
    L = np.where(L,L,np.NaN)
    L = strengths * (L-distances) /L

    # Replace nan by 0, i.e. where L was 0
    L = np.nan_to_num(L)

    D *= L.reshape(len(L),1)
    K = sources['weight'] / (sources['weight'] + targets['weight'])
    K = K.reshape(len(K),1)

    # Note that a direct  nodes['position'][links['source']] += K*D*(1-F)
    # would't work as expected because of repeated indices
    F = nodes['fixed'][sources_idx].reshape(len(links),1)
    W = K*D*(1-F) * 0.1
    nodes['position'][:,0] += np.bincount(sources_idx, W[:,0], minlength=len(nodes))
    nodes['position'][:,1] += np.bincount(sources_idx, W[:,1], minlength=len(nodes))

    F = nodes['fixed'][targets_idx].reshape(len(links),1)
    W = (1-K)*D*(1-F) * 0.1
    nodes['position'][:,0] -= np.bincount(targets_idx, W[:,0], minlength=len(nodes))
    nodes['position'][:,1] -= np.bincount(targets_idx, W[:,1], minlength=len(nodes))


def repulsion(nodes, links):
    P = nodes['position'][:,:2]
    n = len(P)
    X,Y = P[:,0],P[:,1]
    dX,dY = np.subtract.outer(X,X), np.subtract.outer(Y,Y)
    dist = cdist(P,P)
    dist = np.where(dist, dist, 1)
    D = np.empty((n,n,2))
    D[...,0] = dX/dist
    D[...,1] = dY/dist
    D = np.nan_to_num(D)
    R = D.sum(axis=1)
    L = np.sqrt(((R*R).sum(axis=0)))
    R /= L
    F = nodes['fixed'].reshape(len(nodes),1)
    P += 5*R*(1-F)


def attraction(nodes, links):
    P = nodes['position'][:,:2]
    F = nodes['fixed'].reshape(len(nodes),1)
    P += 0.01*((400,400) - P) * (1-F)


def integration(nodes, links):
    P = nodes['position'][:,:2].copy()
    F = nodes['fixed'].reshape(len(nodes),1)
    nodes['position'][:,:2] -= ((nodes['previous'][:,:2]-P)*.9) * (1-F)
    nodes['previous'][:,:2] = P




window = app.Window(width=800, height=800, color=(1,1,1,1))


@window.event
def on_draw(dt):
    window.clear()
    segments.draw()
    markers.draw()


@window.event
def on_mouse_press(x, y, button):
    global drag, index
    drag = False

    nodes['fixed'] = False
    nodes['weight'] = 1

    P = nodes['position'] -  (x,window.height-y,0)
    D = np.sqrt((P**2).sum(axis=1))
    index = np.argmin(D)
    if D[index] < 10:
        nodes['fixed'][index] = True
        nodes['weight'][index] = 0.01
        drag = True

@window.event
def on_mouse_release(x, y, button):
    global drag, index
    drag = False
    nodes['fixed'] = False
    nodes['weight'] = 1


@window.event
def on_mouse_drag(x, y, dx, dy, button):
    global mouse, index

    nodes['position'][index] = x,window.height-y,0
    markers['position'] = nodes['position']
    src = nodes[links['source']]['position']
    segments['P0'] = np.repeat(src,4, axis=0)
    tgt = nodes[links['target']]['position']
    segments['P1'] = np.repeat(tgt,4, axis=0)



@window.timer(1.0/60)
def on_timer(dt):
    relaxation(nodes,links)
    repulsion(nodes,links)
    attraction(nodes,links)
    integration(nodes,links)

    markers['position'] = nodes['position']
    src = nodes[links['source']]['position']
    segments['P0'] = np.repeat(src,4, axis=0)
    tgt = nodes[links['target']]['position']
    segments['P1'] = np.repeat(tgt,4, axis=0)



nodes,links = graph()

transform = OrthographicProjection(Position3D(), aspect=None) + Viewport()
window.attach(transform)
markers = collections.MarkerCollection(marker='disc', transform=transform)
segments = collections.SegmentCollection('agg', transform=transform)

pos = nodes['position']
markers.append(pos, size=15, linewidth=2, itemsize=1,
               fg_color=(1,1,1,1), bg_color=(1,.5,.5,1))

src = nodes[links['source']]['position']
tgt = nodes[links['target']]['position']
segments.append(src, tgt, linewidth=1.5, itemsize=1,
                color=(0.75,0.75,0.75,1.00))
drag,index = False, -1

app.run()
