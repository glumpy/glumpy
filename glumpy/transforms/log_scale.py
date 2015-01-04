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

 * transforms/log-scale-forward.glsl
"""
import numpy as np
from glumpy import library
from . transform import Transform
from . quantitative_scale import QuantitativeScale


class LogScale(QuantitativeScale):
    """ Log scale transform """

    aliases = { "scale_x"  : "log_scale_x",
                "scale_y"  : "log_scale_y",
                "scale_z"  : "log_scale_z",
                "clamp"    : "log_scale_clamp",
                "base"     : "log_scale_base" }


    def __init__(self, *args, **kwargs):
        """
        Initialize the transform.
        Note that parameters must be passed by name (param=value).

        Kwargs parameters
        -----------------

        base : float (default is 10)
            Log base

        domain : tuple of 2 floats (default is (1,10))
            Input domains for xyz

        range : tuple of 2 floats (default is (-1,1))
            Output ranges for xyz

        clamp : bool (default is True)
           Clamping test for xyz
        """

        self._bases = np.ones(3, dtype=np.float32)
        self._bases[...] = Transform._get_kwarg("base", kwargs) or 10

        kwargs["domain"] = kwargs.get("domain", (1,10))
        code = library.get("transforms/log-scale-forward.glsl")
        QuantitativeScale.__init__(self, code, *args, **kwargs)


    @property
    def base(self):
        """ Input base for xyz """
        return self._bases

    @base.setter
    def base(self, value):
        self._bases[...] = np.abs(value)
        if self.is_attached:
            self["base"] = self._bases
            self["scale_x"] = self._x_scale()
            self["scale_y"] = self._y_scale()
            self["scale_z"] = self._z_scale()

    def on_attach(self, program):
        """ Initialization event """

        QuantitativeScale.on_attach(self, program)
        self["base"] = self._bases


    def _scale(self,index):
        scale = self._scales[index].copy()
        domain = scale[:2]
        base = self._bases[index]
        scale[:2] = np.copysign(1,domain) * np.log(np.abs(domain))/np.log(base)
        return scale

    def _x_scale(self): return self._scale(0)

    def _y_scale(self): return self._scale(1)

    def _z_scale(self): return self._scale(2)
