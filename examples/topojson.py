#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import re
import json
import triangle
import numpy as np
from itertools import chain
from glumpy import app, gl, data
from glumpy.graphics.collections import PathCollection, PolygonCollection
from glumpy.transforms import Position, OrthographicProjection, PanZoom, Viewport


def relative_to_absolute(arc, scale=None, translate=None):
    if scale and translate:
        a, b = 0, 0
        for ax, bx in arc:
            a += ax
            b += bx
            yield scale[0]*a + translate[0], scale[1]*b + translate[1]
    else:
        for x, y in arc:
            yield x, y

def convert_coordinates(arcs, topology_arcs, scale=None, translate=None):
    if isinstance(arcs[0], int):
        coords = [
            list(
                relative_to_absolute(
                    topology_arcs[arc if arc >= 0 else ~arc],
                    scale,
                    translate )
                 )[::arc >= 0 or -1][i > 0:] \
            for i, arc in enumerate(arcs) ]
        return list(chain.from_iterable(coords))
    elif isinstance(arcs[0], (list, tuple)):
        return list(
            convert_coordinates(arc, topology_arcs, scale, translate) for arc in arcs)
    else:
        raise ValueError("Invalid input %s", arcs)

def geometry(obj, topology_arcs, scale=None, translate=None):
    return {
        "type": obj['type'],
        "coordinates": convert_coordinates(
            obj['arcs'], topology_arcs, scale, translate )}



window = app.Window(1000, 1000, color=(1,1,1,1))

@window.event
def on_draw(dt):
    window.clear()
    #polygons.draw()
    paths.draw()


transform = PanZoom(OrthographicProjection(Position()), aspect=None)
paths = PathCollection("agg+", transform=transform, linewidth='shared', color="shared")

with open(data.get("us.json"), 'r') as file:
    topology = json.load(file)

scale = topology['transform']['scale']
translate = topology['transform']['translate']
arcs = topology["arcs"]

linewidth = 2.5
color = 0.0,0.0,0.0,1.0
land = topology["objects"]["land"]
for coords in geometry(land, arcs, scale, translate)["coordinates"]:
    for path in coords:
        V = np.zeros((len(path),3))
        V[:,:2] = np.array(path)
        paths.append(V, closed=True, color=color, linewidth=linewidth)

linewidth = 1.0
color = 0.0,0.0,0.0,1.0
for state in topology["objects"]["states"]["geometries"]:
    if state["type"] == "Polygon":
        P = geometry(state, arcs, scale, translate)["coordinates"][0]
        V = np.zeros((len(P),3))
        V[:,:2] = P
        paths.append(V, closed=True, color=color, linewidth=linewidth)
    elif state["type"] == "MultiPolygon":
        for P in geometry(state, arcs, scale, translate)["coordinates"]:
            V = np.zeros((len(P[0]),3))
            V[:,:2] = P[0]
            paths.append(V, closed=True, color=color, linewidth=linewidth)

linewidth = 0.5
color = 0.5,0.5,0.5,1.0
for county in topology["objects"]["counties"]["geometries"]:
    if county["type"] == "Polygon":
        P = geometry(county, arcs, scale, translate)["coordinates"][0]
        V = np.zeros((len(P),3))
        V[:,:2] = P
        paths.append(V, closed=True, color=color, linewidth=0.5)
    elif county["type"] == "MultiPolygon":
        for P in geometry(county, arcs, scale, translate)["coordinates"]:
            V = np.zeros((len(P[0]),3))
            V[:,:2] = P[0]
            paths.append(V, closed=True, color=color, linewidth=linewidth)

window.attach(paths["transform"])
window.attach(paths["viewport"])
app.run()
