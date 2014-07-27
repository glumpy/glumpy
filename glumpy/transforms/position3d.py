# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
from . transform import Transform


class Position3D(Transform):
    def __init__(self):
        Transform.__init__(self, "position-3d.glsl")
