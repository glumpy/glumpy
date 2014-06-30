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

    Parameters
    ----------

    base : floar or tuple
       Logartihmic base for x,y,z
    """

    def __init__(self, base):
        Transform.__init__(self)
        self._base = base

    def forward(self, P):
        """ Forward transformation """

        shape = P.shape
        if len(shape) == 1:
            P = P.reshape(shape[0],1)
        R = P.copy()

        for i in range(R.shape[-1]):
            if self._base[i] > 1.0:
                R[...,i] = np.log(P[...,i]) / np.log(self._base[i])
        return R

    def inverse(self, P):
        """ Inverse transformation """
        shape = P.shape
        if len(shape) == 1:
            P = P.reshape(shape[0],1)
        R = P.copy()

        for i in range(R.shape[-1]):
            if self._base[i] > 1.0:
                R[...,i] = np.power(self._base[i], P[...,i])
        return R

    @property
    def base(self):
        return self._base

    @base.setter
    def base(self, value):
        self._base = value
        if self._program:
            self._program[self.lookup("base")] = self._base
