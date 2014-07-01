#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy.transforms.transform import Transform


class Rotate(Transform):
    """
    Rotation transform
    """

    def __init__(self, theta=0):
        Transform.__init__(self, "rotate.glsl")
        self._base = float(theta)

    @property
    def theta(self):
        return self._theta

    @theta.setter
    def theta(self, value):
        self._theta[...] = value
        self.update("theta")
