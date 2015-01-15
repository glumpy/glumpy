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
            Input domains

        range : tuple of 2 floats (default is (-1,1))
            Output range

        clamp : bool (default is False)
           Clamping test

        discard : bool (default is True)
           Discard test
        """
        domain  = Transform._get_kwarg("domain", kwargs) or (-1,+1)
        range   = Transform._get_kwarg("range", kwargs) or (-1,+1)
        clamp   = Transform._get_kwarg("clamp", kwargs)
        if clamp is None:
            clamp = False
        discard = Transform._get_kwarg("discard", kwargs)
        if discard is None:
            discard = True
        Transform.__init__(self, code, *args, **kwargs)

        self._clamp   = clamp
        self._discard = discard
        self._domain  = np.asarray(domain,dtype=np.float32)
        self._range   = np.asarray(range,dtype=np.float32)


    @property
    def domain(self):
        """ Input domain """

        return self._domain

    @domain.setter
    def domain(self, value):
        """ Input domain """

        self._domain = np.asarray(value,dtype=np.float32)
        if self.is_attached:
            self["domain"] = self._process_domain()


    @property
    def range(self):
        """ Output range for xyz """

        return self._range


    @range.setter
    def range(self, value):
        """ Output range for xyz """

        self._range = np.asarray(value, dtype=np.float32)
        if self.is_attached:
            self["range"] = self._process_range()

    @property
    def clamp(self):
        """ Whether to clamp value """

        return self._clamp


    @clamp.setter
    def clamp(self, value):
        """ Whether to clamp value """

        self._clamp = value
        if self.is_attached:
            self["clamp"] = self._clamp


    @property
    def discard(self):
        """ Whether to discard value (fragment shader only) """

        return self._discard


    @discard.setter
    def discard(self, value):
        """ Whether to discard value (fragment shader only) """

        self._discard = value
        if self.is_attached:
            self["discard"] = self._discard


    def _process_range(self):
        # To be overridden
        return self._range

    def _process_domain(self):
        # To be overridden
        return self._domain


    def on_attach(self, program):
        """ Initialization event """

        self["discard"] = self._discard
        self["clamp"]   = self._clamp
        self["range"]   = self._process_range()
        self["domain"]  = self._process_domain()
