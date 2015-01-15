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

Relevant shader code:

 * transforms/linear-scale-forward.glsl

"""
import numpy as np
from glumpy import library
from . transform import Transform
from . quantitative_scale import QuantitativeScale


class LinearScale(QuantitativeScale):
    """ Linear scale transform """

    aliases = { "domain"  : "linear_scale_domain",
                "range"   : "linear_scale_range",
                "clamp"   : "linear_scale_clamp",
                "discard" : "linear_scale_discard" }


    def __init__(self, *args, **kwargs):
        """
        Initialize the transform.
        Note that parameters must be passed by name (param=value).

        Kwargs parameters
        -----------------

        domain : tuple of 2 floats (default is (-1,1))
            Input domain

        range : tuple of 2 floats (default is (-1,1))
            Output range

        clamp : bool (default is False)
           Clamping test

        discard : bool (default is False)
           Discard test
        """
        code = library.get("transforms/linear-scale.glsl")
        QuantitativeScale.__init__(self, code, *args, **kwargs)
