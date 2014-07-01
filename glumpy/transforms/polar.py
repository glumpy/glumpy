#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
from glumpy.transforms.transform import Transform


class PolarTransform(Transform):
    """
    Polar transform
    """

    def __init__(self):
        Transform.__init__(self, "polar.glsl")
