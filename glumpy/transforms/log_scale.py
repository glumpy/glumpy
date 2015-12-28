# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import library
from . transform import Transform
from . quantitative_scale import QuantitativeScale


class LogScale(QuantitativeScale):
    """
    Log scales are similar to linear scales, except there's a logarithmic
    transform that is applied to the input domain value before the output range
    value is computed. The mapping to the output range value y can be expressed
    as a function of the input domain value x: y = m log(x) + b.

    As log(0) is negative infinity, a log scale must have either an
    exclusively-positive or exclusively-negative domain; the domain must not
    include or cross zero. A log scale with a positive domain has a
    well-defined behavior for positive values, and a log scale with a negative
    domain has a well-defined behavior for negative values (the input value is
    multiplied by -1, and the resulting output value is also multiplied by
    -1). The behavior of the scale is undefined if you pass a negative value to
    a log scale with a positive domain or vice versa.


    :param 2-tuple domain: Input domains. Default is (-1,+1).
    :param 2-tuple range: Output range. Default is (-1,+1).
    :param float base: Log base. Default is 10.
    :param bool clamp: Clamping test. Default is False.
    :param bool discard: Discard test. Default is True.
    """

    aliases = { "domain"  : "log_scale_domain",
                "range"   : "log_scale_range",
                "clamp"   : "log_scale_clamp",
                "base"    : "log_scale_base",
                "discard" : "log_scale_discard" }


    def __init__(self, *args, **kwargs):
        """
        Initialize the transform
        """

        self._base = float(Transform._get_kwarg("base", kwargs) or 10.0)
        kwargs["domain"] = kwargs.get("domain", (1,10))
        code = library.get("transforms/log-scale.glsl")
        QuantitativeScale.__init__(self, code, *args, **kwargs)



    @property
    def base(self):
        """ Input base """
        return self._base


    @base.setter
    def base(self, value):
        """ Input base """
        self._base = np.abs(float(value))
        if self.is_attached:
            self["base"] = self._base
            self["domain"] = self._process_domain()


    def on_attach(self, program):
        QuantitativeScale.on_attach(self, program)
        self["base"] = self._base


    def _scale(self,index):
        domain = self._domain
        base = self._base
        return np.copysign(1.0,domain) * np.log(np.abs(domain))/np.log(base)
