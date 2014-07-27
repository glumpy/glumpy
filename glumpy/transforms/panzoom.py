#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import numpy as np
from . import Transform


class PanZoom(Transform):

    # uniform vec2 scale
    # uniform vec2 translate
    shaderfile = "panzoom.glsl"

    def __init__(self, *args, **kwargs):
        Transform.__init__(self, *args, **kwargs)

        # Local copy of uniform since snippet mat not yet be attached to a program
        self.scale     = np.array([1.,1.])
        self.translate = np.array([0.,0.])

    def on_resize(self, width, height):
        self.width, self.height = float(width), float(height)
        ratio = self.width/self.height
        if ratio > 1.0:
            self.aspect = 1.0/ratio, 1.0
        else:
            self.aspect = 1.0, ratio/1.0
        self["scale"] = self.scale * self.aspect

    def on_mouse_scroll(self, x, y, dx, dy):
        x = x/(self.width/2) - 1
        y = 1 - y/(self.height/2)
        s = np.minimum(np.maximum(self.scale*(1+dy/100), 0.1), 100)
        self.translate[0] = x - s[0] * (x - self.translate[0]) / self.scale[0]
        self.translate[1] = y - s[1] * (y - self.translate[1]) / self.scale[1]
        self.scale = s
        self["scale"] = self.scale * self.aspect
        self["translate"] = self.translate

    def on_mouse_drag(self, x, y, dx, dy, button):
        self.translate += (2*dx/self.width, -2*dy/self.height)
        self["translate"] = self.translate

    def reset(self):
        self.scale = np.array([1.,1.])
        self.translate = np.array([0.,0.])
        self["scale"] = self.aspect * np.array([1.,1.])
        self["translate"] = np.array([0.,0.])


# class LinearScale(Transform):

#     # uniform vec3 scale
#     shaderfile = "linear-scale-forward.glsl"


#     def __init__(self, *args, **kwargs):
#         Transform.__init__(self, *args, **kwargs)


#     @property
#     def scale(self):
#         return self['scale']

#     @scale.setter
#     def scale(self, value):
#         self['scale'] = value
