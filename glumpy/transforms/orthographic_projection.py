# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
from glumpy import glm
from . import Transform


class OrthographicProjection(Transform):

    # uniform mat4 projection
    shaderfile = "projection.glsl"


    def __init__(self, *args, **kwargs):
        Transform.__init__(self, *args, **kwargs)


    def on_resize(self, width, height):
        self["projection"] = glm.ortho(0, width, 0, height, +1,-1)
