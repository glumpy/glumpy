# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
from glumpy import glm, library
from . transform import Transform

class OrthographicProjection(Transform):

    def __init__(self, *args, **kwargs):
        code = library.get("transforms/projection.glsl")
        Transform.__init__(self, code, *args, **kwargs)

    def on_resize(self, width, height):
        self["projection"] = glm.ortho(0, width, 0, height, +1000,-1000)
        Transform.on_resize(self, width, height)
