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

    def __init__(self, scale=(1.0,1.0,1.0)):
        Transform.__init__(self, "./linear_scale.glsl")
        self._scale = np.array(scale)

    def forward(self, P):
        """ Forward transformation """
        return P * self._scale

    def inverse(self, P):
        """ Inverse transformation """
        return P / self._scale

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value
        self._program[self.lookup("scale")] = self._scale
