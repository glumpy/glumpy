# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import csv, json
import numpy as np
from glumpy import app, gl, data
from glumpy.transforms import *
from glumpy.graphics.collections import *


# Building the transformation
# ---------------------------
scale = 2*1285.0
Lower48 = ConicEqualArea(scale = scale,    parallels = (29.5, 45.5),
                         rotate = (96,0),  center = (0.38, -0.41))
Alaska = ConicEqualArea(scale=scale/3,     parallels = (55, 65),
                        rotate = (154, 0), center = (.32, -.8),
                        clip = [-200, +200, +50, 100] )
Hawai = ConicEqualArea(scale=scale,        parallels = (8, 18),
                        rotate = (157, 0), center = (.24, -.32),
                        clip = [-180, -140, -90, +90] )

transform = Position(Lower48(Hawai(Alaska(GeoPosition()))))
transform = PanZoom(OrthographicProjection(transform))


# Building collection using extended dtype and our own fragment 
# -------------------------------------------------------------
fragment = """
#include "colormaps/colormaps.glsl"
varying float rate;
void main(void)
{
    gl_FragColor = vec4(colormap_autumn(1-rate),1.0);
}
"""
paths = PathCollection("agg+", transform=transform, linewidth='shared', color="shared")
polys = PolygonCollection("raw", transform=transform, color="shared", fragment=fragment,
                          user_dtype=[('rate', (np.float32, 1), 'shared', 0.0)])


# Opening the topojson file
# -------------------------
with open(data.get("us.json"), 'r') as file:
    geomap = json.load(file)
arcs = geomap["arcs"]
scale = geomap['transform']['scale']
translate = geomap['transform']['translate']

# Apply scale and transform all coordinates (= arcs)
_arcs = []
for arc in arcs:
    _arc = []
    x, y = translate[0], translate[1]
    for position in arc:
        x = x + position[0]*scale[0] 
        y = y + position[1]*scale[1] 
        _arc.append((x,y))
    _arcs.append(_arc)
arcs = _arcs

# A polygon is made of one or several rings, a ring is made of arcs
# If there is several rings, the first is the exterior ring while the others are holes
def build_paths(obj):
    paths = []
    if obj["type"] == "Polygon": polygons = [obj["arcs"]]
    else:                        polygons =  obj["arcs"]
    for polygon in polygons:
        for ring in polygon:
            path = []
            for i,arc in enumerate(ring):
                if i == 0:
                    if arc >= 0: path.extend(arcs[arc])
                    else:        path.extend((arcs[~arc])[::-1])
                else:
                    if arc >= 0: path.extend(arcs[arc][1:])
                    else:        path.extend((arcs[~arc][:-1])[::-1])
            if len(path) > 2:
                V = np.zeros((len(path),3), dtype=np.float32)
                V[:,:2] = np.array(path)
                paths.append(V)
    return paths


# Opening the unemployment rate
# -----------------------------
unemployment = {}
with open(data.get('us-unemployment.tsv'), 'r') as file:
    reader = csv.reader(file, delimiter='\t')
    next(reader, None) # skip the header
    for row in reader:
        unemployment[int(row[0])] = float(row[1]) / 0.16

                     
# Building the chloropleth
# ------------------------
# We could exploit the topojson format to restrict path drawing to
# non-overlapping paths

# State counties
for county in geomap["objects"]["counties"]["geometries"]:
    for V in build_paths(county):
        paths.append(V, closed=True, color=(1,1,1,.5), linewidth=1.0)
        if len(V) > 3:
            key = county["id"]
            rate = 0.0
            if key in unemployment.keys():
                rate = unemployment[county["id"]]
            polys.append(V[:-1], color=(1,1,1,1), rate=rate)

# Federal states
for state in geomap["objects"]["states"]["geometries"]:
    for V in build_paths(state):
        paths.append(V, closed=True, color=(.25,.25,.25,1), linewidth=0.75)

# USA land
for V in build_paths(geomap["objects"]["land"]):
    paths.append(V, closed=True, color=(0,0,0,1), linewidth=1.5)


window = app.Window(2*960, 2*600, color=(1,1,1,1))

@window.event
def on_draw(dt):
    window.clear()
    polys.draw(), paths.draw()

window.attach(paths["transform"])
window.attach(paths["viewport"])
app.run()
