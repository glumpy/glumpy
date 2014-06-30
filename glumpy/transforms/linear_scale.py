#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy.transforms.transform import Transform


class LinearScale(Transform):
    """
    Linear scaling transform
    """

    def __init__(self, scale=(1,1,1)):
        Transform.__init__(self, "linear_scale.glsl")
        self._scale = np.zeros(3,np.float32)
        self._scale[...] = scale

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale[...] = value
        self.update("scale")
