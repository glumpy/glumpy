# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import library
from . transform import Transform
from . quantitative_scale import QuantitativeScale


class PowerScale(QuantitativeScale):
    """
    Power scales are similar to linear scales, except there's an exponential
    transform that is applied to the input domain value before the output range
    value is computed. The mapping to the output range value y can be expressed
    as a function of the input domain value x: y = mx^k + b, where k is the
    exponent value. Power scales also support negative values, in which case
    the input value is multiplied by -1, and the resulting output value is also
    multiplied by -1.

    :param 2-tuple domain: Input domains. Default is (-1,+1).
    :param 2-tuple range: Output range. Default is (-1,+1).
    :param float exponent: Power exponent. Default is 1.
    :param bool clamp: Clamping test. Default is False.
    :param bool discard: Discard test. Default is True.
    """

    aliases = { "domain"   : "power_scale_domain",
                "range"    : "power_scale_range",
                "clamp"    : "power_scale_clamp",
                "discard"  : "power_scale_discard",
                "exponent" : "power_scale_exponent" }


    def __init__(self, *args, **kwargs):
        """
        Initialize the transform.
        """

        self._exponents = Transform._get_kwarg("exponent", kwargs, 1.0)
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
        QuantitativeScale.on_attach(self, program)
        self["exponent"] = self._exponents


    def _process_domain(self):
        domain = self._domain
        exponent = self._exponents
        domain = np.copysign(1,domain) * np.power(np.abs(domain), exponent)
        return domain
