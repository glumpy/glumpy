#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
"""
Linear scale transform

  Linear scales are the most common scale, and a good default choice to map a
  continuous input domain to a continuous output range. The mapping is linear
  in that the output range value y can be expressed as a linear function of the
  input domain value x: y = mx + b. The input domain is typically a dimension
  of the data that you want to visualize, such as the height of students
  (measured in meters) in a sample population. The output range is typically a
  dimension of the desired output visualization, such as the height of bars
  (measured in pixels) in a histogram.

The transform is connected to the following events:

 * attach (initialization)
 * data (update)

Relevant shader code:

 * transforms/linear-scale-forward.glsl

"""
import numpy as np
from glumpy import library
from . transform import Transform


class LinearScale(Transform):
    """ Linear scale transform """

    aliases = { "x"     : "linear_scale_x",
                "y"     : "linear_scale_y",
                "z"     : "linear_scale_z",
                "clamp" : "linear_scale_clamp" }


    def __init__(self, *args, **kwargs):
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

        code = library.get("transforms/linear-scale-forward.glsl")
        Transform.__init__(self, code, *args, **kwargs)

        self._scales = np.zeros((3,4), dtype=np.float32)
        self._scales[0] = -1,+1, -1,+1
        self._scales[1] = -1,+1, -1,+1
        self._scales[2] = -1,+1, -1,+1
        self._clamp  = False

        self.domain = Transform._get_kwarg("domain", kwargs) or (-1,+1)
        self.range = Transform._get_kwarg("range", kwargs) or (-1,+1)
        self.clamp =  Transform._get_kwarg("clamp", kwargs) or False


    @property
    def domain(self):
        """ Input domain for xyz """
        return self._scales[:,:2]

    @domain.setter
    def domain(self, value):
        self._scales[:,:2] = value
        if self.is_attached:
            self["linear_scale_x"] = self._scales[0]
            self["linear_scale_y"] = self._scales[1]
            self["linear_scale_z"] = self._scales[2]

    @property
    def xdomain(self):
        """ Input domain for x"""
        return self._scales[0,:2]

    @xdomain.setter
    def xdomain(self, value):
        self._scales[0,:2] = value
        if self.is_attached:
            self["linear_scale_x"] = self._scales[0]

    @property
    def ydomain(self):
        """ Input domain for y"""
        return self._scales[1,:2]

    @ydomain.setter
    def ydomain(self, value):
        self._scales[1,:2] = value
        if self.is_attached:
            self["linear_scale_y"] = self._yscale

    @property
    def zdomain(self):
        """ Input domain for z"""
        return self._scales[2,:2]

    @zdomain.setter
    def zdomain(self, value):
        self._scales[2,:2] = value
        if self.is_attached:
            self["linear_scale_z"] = self._scales[2]

    @property
    def range(self):
        """ Output range for xyz"""

        return self._scales[:,2:]

    @range.setter
    def range(self, value):
        self._scales[:,2:] = value

        if self.is_attached:
            self["linear_scale_x"] = self._scales[0]
            self["linear_scale_y"] = self._scales[1]
            self["linear_scale_z"] = self._scales[2]

    @property
    def xrange(self):
        """ Input range for x"""
        return self._scales[0,2:]

    @xrange.setter
    def xrange(self, value):
        self._scales[0,2:] = value
        if self.is_attached:
            self["linear_scale_x"] = self._scales[0]

    @property
    def yrange(self):
        """ Input range for y"""
        return self._scales[1,2:]

    @yrange.setter
    def yrange(self, value):
        self._scales[1,2:] = value
        if self.is_attached:
            self["linear_scale_y"] = self._scales[1]

    @property
    def zrange(self):
        """ Input range for z"""
        return self._scales[2,2:]

    @zrange.setter
    def zrange(self, value):
        self._scales[2,2:] = value
        if self.is_attached:
            self["linear_scale_z"] = self._scales[2]

    @property
    def clamp(self):
        """ Whether to clamp xyz values """
        return self._clamp

    @clamp.setter
    def clamp(self, value):
        self._clamp = value
        if self.is_attached:
            self["clamp"] = self._clamp


    def __getitem__(self, key):
        """ Override getitem to enforce aliases """

        if key in LinearScale.aliases.keys():
            key = LinearScale.aliases[key]
            return getattr(self,key)
        return Transform.__getitem__(self, key)


    def __setitem__(self, key, value):
        """ Override getitem to enforce aliases """

        if key in LinearScale.aliases.keys():
            key = LinearScale.aliases[key]
            setattr(self,key,value)
        else:
            Transform.__setitem__(self, key, value)


    def on_attach(self, program):
        """ Initialization event """

        self["linear_scale_clamp"] = self._clamp
        self["linear_scale_x"] = self._scales[0]
        self["linear_scale_y"] = self._scales[1]
        self["linear_scale_z"] = self._scales[2]
