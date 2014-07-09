# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
from glumpy import glm
from glumpy.transforms.transform import Transform


class OrthographicProjection(Transform):
    """
    Orthographic projection
    """

    def __init__(self):
        Transform.__init__(self, "matrix.glsl")

    def on_resize(self, width, height):
        self["matrix"] = glm.ortho(0, width, 0, height, +1,-1)
