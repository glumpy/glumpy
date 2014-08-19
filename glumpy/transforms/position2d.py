# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
from . transform import Transform
from glumpy.shaders import get_code

class Position2D(Transform):

    def __init__(self, *args, **kwargs):
        code = get_code("position-2d.glsl")
        Transform.__init__(self, code, *args, **kwargs)
