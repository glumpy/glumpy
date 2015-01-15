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

    aliases = { "domain"   : "power_scale_domain",
                "range"    : "power_scale_range",
                "clamp"    : "power_scale_clamp",
                "discard"  : "power_scale_discard",
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
            Input domain

        range : tuple of 2 floats (default is (-1,1))
            Output range

        clamp : bool (default is False)
           Clamping test

        discard : bool (default is False)
           Discard test
        """

        self._exponents = Transform._get_kwarg("exponent", kwargs) or 1.0
        code = library.get("transforms/power-scale.glsl")
        QuantitativeScale.__init__(self, code, *args, **kwargs)


    @property
    def exponent(self):
        """ Input exponent for xyz """
        return self._exponents


    @exponent.setter
    def exponent(self, value):
        self._exponents = abs(float(value))
        if self.is_attached:
            self["exponent"] = self._exponents
            self["domain"] = self._process_domain()


    def on_attach(self, program):
        """ Initialization event """

        QuantitativeScale.on_attach(self, program)
        self["exponent"] = self._exponents


    def _process_domain(self):
        domain = self._domain
        exponent = self._exponents
        domain = np.copysign(1,domain) * np.power(np.abs(domain), exponent)
        return domain
