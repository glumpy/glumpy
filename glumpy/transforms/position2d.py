# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
from . import Transform

class Position2D(Transform):

    shaderfile = "position-2d.glsl"

    def __init__(self, *args, **kwargs):
        Transform.__init__(self, *args, **kwargs)
