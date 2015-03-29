# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
"""
Albers projection

See: https://github.com/mbostock/d3/blob/master/src/geo/conic-equal-area.js
     http://mathworld.wolfram.com/AlbersEqual-AreaConicProjection.html
     http://en.wikipedia.org/wiki/Albers_projection

"""
from glumpy import library
from . transform import Transform


class AlbersProjection(Transform):
    """ Albers projection """

    aliases = {  }

    def __init__(self, *args, **kwargs):
        """
        Initialize the transform.
        Note that parameters must be passed by name (param=value).

        Kwargs parameters
        -----------------
        """

        code = library.get("transforms/albers.glsl")
        Transform.__init__(self, code, *args, **kwargs)


    def on_attach(self, program):
        """ Initialization event """
        pass
