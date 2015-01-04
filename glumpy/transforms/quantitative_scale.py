#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
"""
Abstract quantitative scale

Scales are functions that map from an input domain to an output
range. Quantitative scales have a continuous domain, such as the set of real
numbers, or dates. There are also ordinal scales, which have a discrete
domain, such as a set of names or categories.

The transform is connected to the following events:

 * attach (initialization)

"""
import numpy as np
from glumpy import library
from . transform import Transform


class QuantitativeScale(Transform):
    """ Quantitative scale transform (abstract class) """

    aliases = { }


    def __init__(self, code, *args, **kwargs):
        """
        Initialize the transform.
        Note that parameters must be passed by name (param=value).

        Kwargs parameters
        -----------------

        domain : tuple of 2 floats (default is (-1,1))
            Input domains for xyz

        range : tuple of 2 floats (default is (-1,1))
            Output ranges for xyz

        clamp : bool (default is True)
           Clamping test for xyz
        """

        Transform.__init__(self, code, *args, **kwargs)

        self._clamp = False
        self._scales = np.zeros((3,4), dtype=np.float32)
        self._scales[0] = -1,+1, -1,+1
        self._scales[1] = -1,+1, -1,+1
        self._scales[2] = -1,+1, -1,+1

        self.domain = Transform._get_kwarg("domain", kwargs) or (-1,+1)
        self.range  = Transform._get_kwarg("range", kwargs) or (-1,+1)
        self.clamp  = Transform._get_kwarg("clamp", kwargs) or False


    @property
    def domain(self):
        """ Input domain for xyz """

        return self._scales[:,:2]

    @domain.setter
    def domain(self, value):
        """ Input domain for xyz """

        self._scales[:,:2] = value
        if self.is_attached:
            self["linear_scale_x"] = self._x_scale()
            self["linear_scale_y"] = self._y_scale()
            self["linear_scale_z"] = self._z_scale()

    @property
    def range(self):
        """ Output range for xyz """

        return self._scales[:,2:]


    @range.setter
    def range(self, value):
        """ Output range for xyz """

        self._scales[:,2:] = value
        if self.is_attached:
            self["linear_scale_x"] = self._x_scale()
            self["linear_scale_y"] = self._y_scale()
            self["linear_scale_z"] = self._z_scale()

    @property
    def clamp(self):
        """ Whether to clamp xyz values """

        return self._clamp


    @clamp.setter
    def clamp(self, value):
        """ Whether to clamp xyz values """

        self._clamp = value
        if self.is_attached:
            self["clamp"] = self._clamp


    def __getitem__(self, key):
        """ Override getitem to enforce aliases """

        key = self.__class__.aliases.get(key, key)
        return Transform.__getitem__(self, key)


    def __setitem__(self, key, value):
        """ Override getitem to enforce aliases """

        key = self.__class__.aliases.get(key, key)
        Transform.__setitem__(self, key, value)


    def _x_scale(self):
        # To be overridden
        return self._scales[0]

    def _y_scale(self):
        # To be overridden
        return self._scales[1]

    def _z_scale(self):
        # To be overridden
        return self._scales[2]

    def on_attach(self, program):
        """ Initialization event """

        self["clamp"]   = self._clamp
        self["scale_x"] = self._x_scale()
        self["scale_y"] = self._y_scale()
        self["scale_z"] = self._z_scale()
