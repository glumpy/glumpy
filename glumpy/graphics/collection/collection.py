# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
""" """

import os
import numpy as np
from functools import reduce
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

        for (name,gtype) in self._program.all_uniforms:
            if name == key:
                return self._program[key]
        return BaseCollection.__getitem__(self, key)


    def __setitem__(self, key, value):

        for (name,gtype) in self._program.all_uniforms:
            if name == key:
                self._program[key] = value
                return
        BaseCollection.__setitem__(self, key, value)
