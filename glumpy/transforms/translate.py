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

    Parameters
    ----------

    translate : float or tuple
       Translation factor for x,y,z coordinates
    """

    def __init__(self, translate=(0.0,0.0,0.0)):
        Transform.__init__(self, "./translate.glsl")
        self._translate = translate

    def forward(self, P):
        """ Forward transformation """
        return P + self._translate

    def inverse(self, P):
        """ Inverse transformation """
        return P - self._translate

    @property
    def translate(self):
        return self._translate

    @translate.setter
    def translate(self, value):
        self._translate = value
        if self._program:
            self._program[self.lookup("translate")] = self._translate
