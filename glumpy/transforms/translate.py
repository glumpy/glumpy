#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy.transforms.transform import Transform


class Translate(Transform):
    """
    Translation transform
    """

    def __init__(self, translate=(0,0,0)):
        Transform.__init__(self, "translate.glsl")
        self._translate = np.zeros(3,np.float32)
        self._translate[...] = translate

    @property
    def translate(self):
        return self._translate

    @translate.setter
    def translate(self, value):
        self._translate[...] = value
        self.update("translate")
