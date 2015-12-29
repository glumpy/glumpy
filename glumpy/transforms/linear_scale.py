# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import library
from . transform import Transform
from . quantitative_scale import QuantitativeScale


class LinearScale(QuantitativeScale):
    """
    Linear scales are the most common scale, and a good default choice to map a
    continuous input domain to a continuous output range. The mapping is linear
    in that the output range value y can be expressed as a linear function of
    the input domain value x: y = mx + b. The input domain is typically a
    dimension of the data that you want to visualize, such as the height of
    students (measured in meters) in a sample population. The output range is
    typically a dimension of the desired output visualization, such as the
    height of bars (measured in pixels) in a histogram.

    :param 2-tuple domain: Input domains. Default is (-1,+1).
    :param 2-tuple range: Output range. Default is (-1,+1).
    :param bool clamp: Clamping test. Default is False.
    :param bool discard: Discard test. Default is True.
    """

    aliases = { "domain"  : "linear_scale_domain",
                "range"   : "linear_scale_range",
                "clamp"   : "linear_scale_clamp",
                "discard" : "linear_scale_discard" }

    def __init__(self, *args, **kwargs):
        """
        Initialize the transform.
        """
        code = library.get("transforms/linear-scale.glsl")
        QuantitativeScale.__init__(self, code, *args, **kwargs)
