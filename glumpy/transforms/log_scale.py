#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy.transforms.transform import Transform


class LogScale(Transform):
    """
    Logarithmic scaling transform
    """

    def __init__(self, base = (0,0,0)):
        Transform.__init__(self, "log_scale.glsl")
        self["base"] = np.zeros(3, np.float32)
        self["base"][...] = base
