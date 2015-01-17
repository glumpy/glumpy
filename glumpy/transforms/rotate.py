#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import math
import numpy as np
from glumpy import library
from glumpy.transforms.transform import Transform


def _rotation(angle, x, y, z):
    angle = math.pi * angle / 180
    c, s = math.cos(angle), math.sin(angle)
    n = math.sqrt(x * x + y * y + z * z)
    x,y,z = x/n, y/n, z/n
    cx, cy, cz = (1 - c) * x, (1 - c) * y, (1 - c) * z
    return np.array([[cx * x + c, cy * x - z * s, cz * x + y * s, 0],
                     [cx * y + z * s, cy * y + c, cz * y - x * s, 0],
                     [cx * z - y * s, cy * z + x * s, cz * z + c, 0],
                     [0, 0, 0, 1]], dtype=np.float32).T


class Rotate(Transform):
    """ Rotation transform """

    aliases = { "axis"    : "rotate_axis",
                "angle"   : "rotate_angle",
                "origin"  : "rotate_origin",
                "forward" : "rotate_forward_matrix",
                "inverse" : "rotate_inverse_matrix" }

    def __init__(self, *args, **kwargs):
        """
        Initialize the transform.
        Note that parameters must be passed by name (param=value).

        Kwargs parameters
        -----------------
        """
        self._forward = np.zeros((4,4), dtype=np.float32)
        self._inverse = np.zeros((4,4), dtype=np.float32)
        self._axis = Transform._get_kwarg("axis", kwargs, (0,0,1))
        self._angle = Transform._get_kwarg("angle", kwargs, 0.0)
        self._origin = Transform._get_kwarg("origin", kwargs, (0.,0.,0.))

        print self._origin


        code = library.get("transforms/rotate.glsl")
        Transform.__init__(self, code, *args, **kwargs)

        # Force building of rotation matrices
        self.axis = self._axis

    @property
    def axis(self):
        """ Rotation axis """

        return self._axis

    @axis.setter
    def axis(self, value):
        """ Rotation axis """

        self._axis = np.array(value, dtype=np.float32)
        x,y,z = self._axis
        self._forward = _rotation(+self._angle, x, y, z)
        self._inverse = _rotation(-self._angle, x, y, z)
        if self.is_attached:
            self["axis"] = self._axis
            self["forward"] = self._forward
            self["inverse"] = self._inverse

    @property
    def origin(self):
        """ Rotation origin """

        return self._origin

    @origin.setter
    def origin(self, value):
        """ Rotation origin """

        self._origin = np.array(value, dtype=np.float32)
        if self.is_attached:
            self["origin"] = self._origin


    @property
    def angle(self):
        """ Rotation angle (degrees) """

        return self._angle

    @angle.setter
    def angle(self, value):
        """ Rotation angle (degrees) """

        self._angle = float(value)
        x,y,z = self._axis

        self._forward[...] = _rotation(+self._angle, x, y, z)
        self._inverse[...] = _rotation(-self._angle, x, y, z)
        if self.is_attached:
            self["angle"] = self._angle
            self["forward"] = self._forward
            self["inverse"] = self._inverse


    def on_attach(self, program):
        """ Initialization """

        self["axis"] = self._axis
        self["angle"] = self._angle
        self["origin"] = self._origin
        self["forward"] = self._forward
        self["inverse"] = self._inverse
