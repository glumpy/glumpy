# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
""" """

import os
import numpy as np
from functools import reduce
from glumpy.gloo.program import Program
from glumpy.graphics.collection.util import fetchcode
from glumpy.graphics.collection.base_collection import BaseCollection



class Collection(BaseCollection):

    _gtypes = { ('float32', 1) : "float",
                ('float32', 2) : "vec2",
                ('float32', 3) : "vec3",
                ('float32', 4) : "vec4",
                ('int32', 1)   : "int",
                ('int32', 2)   : "ivec2",
                ('int32', 3)   : "ivec3",
                ('int32', 4)   : "ivec4" }

    def __init__(self, dtypes, scopes, itype=None, **kwargs):

        vtype      = [] # self._vertices
        utype      = [] # self._uniforms

        self._uniforms = {}
        self._attributes = {}
        self._varyings = {}

        declarations = {"uniforms"   : "",
                        "attributes" : "",
                        "varyings"   : ""}
        dtypes = np.dtype(dtypes)
        for name in dtypes.names:
            scope = kwargs.get(name, scopes.get(name, 'local'))
            dtype = dtypes[name].base
            count = np.zeros(dtypes[name].shape).size
            gtype = Collection._gtypes[(dtype.name,count)]

            if scope is "local":
                vtype.append( (name, dtype, count) )
                declarations["attributes"] += "attribute %s %s;\n" % (gtype, name)
            elif scope is "shared":
                utype.append( (name, dtype, count) )
                declarations["varyings"] += "varying %s %s;\n" % (gtype, name)
            else:
                declarations["uniforms"] += "uniform %s %s;\n" % (gtype, name)
                self._uniforms[name] = None

        vtype = np.dtype(vtype)
        itype = np.dtype(itype) if itype else None
        utype = np.dtype(utype) if utype else None
        BaseCollection.__init__(self, vtype=vtype, utype=utype, itype=itype)
        self._declarations = declarations


    def __getitem__(self, key):
        if key in self._uniforms.keys():
            if self._program is not None:
                return self._program[key]
            return self._uniforms[key]
        else:
            return BaseCollection.__getitem__(self, key)


    def __setitem__(self, key, value):

        if key in self._uniforms.keys():
            if self._program is not None:
                self._program[key] = value
            self._uniforms[key] = value
        else:
            BaseCollection.__setitem__(self, key, value)






class MarkerCollection(Collection):

    defaults = { 'position'    : (0.0,0.0,0.0),
                 'size'        : 32.0,
                 'orientation' : 0.0,
                 'fg_color'    : (0,0,0,1),
                 'bg_color'    : (1,1,1,1),
                 'antialias'   : 1.0,
                 'linewidth'   : 1.0 }

    def __init__(self, count=0, marker='cross'):

        # This cannot be changed (shader code depends on it)
        dtypes = [ ('position',    np.float32, 3),
                   ('size',        np.float32, 1),
                   ('orientation', np.float32, 1),
                   ('fg_color',    np.float32, 4),
                   ('bg_color',    np.float32, 4),
                   ('linewidth',   np.float32, 1),
                   ('antialias',   np.float32, 1) ]

        # This can be changed but 'position'
        scopes = { 'position'   : 'local',
                   'size'       : 'local',
                   'orientation': 'local',
                   'fg_color'   : 'local',
                   'bg_color'   : 'local',
                   'linewidth'  : 'global',
                   'antialias'  : 'global' }

        Collection.__init__(self, dtypes, scopes)

        path = os.path.dirname(__file__)
        path = os.path.join(path,'shaders')
        vertex = ""
        if self.utype is not None:
            vertex += fetchcode(self.utype)
        else:
            vertex += "void fetch_uniforms(void) { }\n"
        vertex += self._declarations["uniforms"]
        vertex += self._declarations["attributes"]
        vertex += open(os.path.join(path, 'marker.vert')).read()

        fragment = ""
        fragment += open(os.path.join(path, 'marker-cross.frag')).read()
        fragment += open(os.path.join(path, 'antialias.glsl')).read()
        fragment += open(os.path.join(path, 'marker.frag')).read()

        if count > 0:
            V = np.zeros(count, dtype = self.vtype)
            Collection.append(self, V, itemsize=1)

        self._program = Program(vertex, fragment)
        for name in self._uniforms.keys():
            self._uniforms[name] = MarkerCollection.defaults.get(name)
            self._program[name] = self._uniforms[name]
        self._build_buffers()



    # def append( self, position, size=32.0, orientation = 0.0,
    #                   fg_color = (0,0,0,1), bg_color = (1,1,1,1),
    #                   linewidth = 1.0, antialias = 1.0):
    #     V = np.zeros(1, dtype=self._vertices.dtype)
    #     V['position'] = position
    #     V['orientation'] = orientation
    #     V['size'] = 32
    #     U = np.zeros(1, dtype=self._uniforms.dtype)
    #     U['fg_color'] = 0,0,0,1
    #     U['bg_color'] = 0,0,0,1
    #     Collection.append(self, V, U)


    def draw(self, *args, **kwargs):
        self._program.draw(*args, **kwargs)
