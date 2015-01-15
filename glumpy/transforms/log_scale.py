#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
"""
Log scale transform

Log scales are similar to linear scales, except there's a logarithmic transform
that is applied to the input domain value before the output range value is
computed. The mapping to the output range value y can be expressed as a
function of the input domain value x: y = m log(x) + b.

As log(0) is negative infinity, a log scale must have either an
exclusively-positive or exclusively-negative domain; the domain must not
include or cross zero. A log scale with a positive domain has a well-defined
behavior for positive values, and a log scale with a negative domain has a
well-defined behavior for negative values (the input value is multiplied by -1,
and the resulting output value is also multiplied by -1). The behavior of the
scale is undefined if you pass a negative value to a log scale with a positive
domain or vice versa.

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

    aliases = { "domain"  : "log_scale_domain",
                "range"   : "log_scale_range",
                "clamp"   : "log_scale_clamp",
                "base"    : "log_scale_base",
                "discard" : "log_scale_discard" }


    def __init__(self, *args, **kwargs):
        """
        Initialize the transform.
        Note that parameters must be passed by name (param=value).

        Kwargs parameters
        -----------------

        base : float (default is 10)
            Log base

        domain : tuple of 2 floats (default is (1,10))
            Input domain

        range : tuple of 2 floats (default is (-1,1))
            Output range

        clamp : bool (default is False)
           Clamping test

        discard : bool (default is False)
           Discard test
        """

        self._base = float(Transform._get_kwarg("base", kwargs) or 10.0)
        kwargs["domain"] = kwargs.get("domain", (1,10))
        code = library.get("transforms/log-scale.glsl")
        QuantitativeScale.__init__(self, code, *args, **kwargs)


    @property
    def base(self):
        """ Input base for xyz """
        return self._base


    @base.setter
    def base(self, value):
        self._base = np.abs(float(value))
        if self.is_attached:
            self["base"] = self._base
            self["domain"] = self._process_domain()


    def on_attach(self, program):
        """ Initialization event """

        QuantitativeScale.on_attach(self, program)
        self["base"] = self._base


    def _scale(self,index):
        domain = self._domain
        base = self._base
        return np.copysign(1.0,domain) * np.log(np.abs(domain))/np.log(base)
