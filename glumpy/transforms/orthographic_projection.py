# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
from glumpy import glm
from . transform import Transform
from glumpy.shaders import get_code


class OrthographicProjection(Transform):

    def __init__(self, *args, **kwargs):
        code = get_code("projection.glsl")
        Transform.__init__(self, code, *args, **kwargs)

    def on_resize(self, width, height):
        self["projection"] = glm.ortho(0, width, 0, height, +1,-1)
