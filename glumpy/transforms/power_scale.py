#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
"""
Power scale transform

Power scales are similar to linear scales, except there's an exponential
transform that is applied to the input domain value before the output range
value is computed. The mapping to the output range value y can be expressed as
a function of the input domain value x: y = mx^k + b, where k is the exponent
value. Power scales also support negative values, in which case the input value
is multiplied by -1, and the resulting output value is also multiplied by -1.

The transform is connected to the following events:

 * attach (initialization)

Relevant shader code:

 * transforms/power-scale-forward.glsl
"""
import numpy as np
from glumpy import library
from . transform import Transform
from . quantitative_scale import QuantitativeScale


class PowerScale(QuantitativeScale):
    """ Power scale transform """

    aliases = { "scale_x"  : "power_scale_x",
                "scale_y"  : "power_scale_y",
                "scale_z"  : "power_scale_z",
                "clamp"    : "power_scale_clamp",
                "exponent" : "power_scale_exponent" }


    def __init__(self, *args, **kwargs):
        """
        Initialize the transform.
        Note that parameters must be passed by name (param=value).

        Kwargs parameters
        -----------------

        exponent : float (default is 1)
            Power exponent

        domain : tuple of 2 floats (default is (-1,1))
            Input domains for xyz

        range : tuple of 2 floats (default is (-1,1))
            Output ranges for xyz

        clamp : bool (default is True)
           Clamping test for xyz
        """

        self._exponents = np.ones(3, dtype=np.float32)
        self._exponents[...] = Transform._get_kwarg("exponent", kwargs) or 1
        code = library.get("transforms/power-scale-forward.glsl")
        QuantitativeScale.__init__(self, code, *args, **kwargs)


    @property
    def exponent(self):
        """ Input exponent for xyz """
        return self._exponents

    @exponent.setter
    def exponent(self, value):
        self._exponents[...] = np.abs(value)
        if self.is_attached:
            self["exponent"] = self._exponents
            self["scale_x"] = self._x_scale()
            self["scale_y"] = self._y_scale()
            self["scale_z"] = self._z_scale()

    def on_attach(self, program):
        """ Initialization event """

        QuantitativeScale.on_attach(self, program)
        self["exponent"] = self._exponents


    def _scale(self,index):
        scale = self._scales[index].copy()
        domain = scale[:2]
        exponent = self._exponents[index]
        scale[:2] = np.copysign(1,domain) * np.power(np.abs(domain), exponent)
        return scale

    def _x_scale(self): return self._scale(0)

    def _y_scale(self): return self._scale(1)

    def _z_scale(self): return self._scale(2)
