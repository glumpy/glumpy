#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import gl,library
from . transform import Transform


class PanZoom(Transform):

    def __init__(self, *args, **kwargs):
        code = library.get("transforms/panzoom.glsl")
        Transform.__init__(self, code, *args, **kwargs)

        kwargs["aspect"] = kwargs.get("aspect", 1.0)
        aspect = kwargs["aspect"]
        del kwargs["aspect"]

        self.scale = np.array([1.,1.])
        self.translate = np.array([0.,0.])
        self.bounds = (0.1, 10000.0)
        self.aspect = None
        if aspect is not None:
            self.aspect = aspect*np.ones(2)

    def on_attach(self, program):
        """ A new program is attached """

        self["scale"]     = self.scale
        self["translate"] = self.translate


    def on_resize(self, width, height):
        """ Window has been resized """

        self.width = float(width)
        self.height = float(height)
        ratio = self.width/self.height
        if ratio > 1.0:
            aspect = np.array([1.0/ratio, 1.0])
        else:
            aspect = np.array([1.0, ratio/1.0])
        if aspect is not None:
            if self.aspect is not None:
                self.translate *= aspect / self.aspect
                self.aspect = aspect
                self["scale"] = self.scale * self.aspect
            else:
                self.translate *= aspect
                self["scale"] = self.scale
        else:
            self.translate *= aspect
            self["scale"] = self.scale
        self["translate"] = self.translate
        Transform.on_resize(self, width, height)


    def on_mouse_scroll(self, x, y, dx, dy):
        """ Mouse has been scrolled """

        x = x/(self.width/2.) - 1.
        y = 1. - y/(self.height/2.)

        scale_min, scale_max = self.bounds
        s = np.minimum(np.maximum(self.scale*(1+dy/100.0), scale_min), scale_max)
        self.translate[0] = x - s[0] * (x - self.translate[0]) / self.scale[0]
        self.translate[1] = y - s[1] * (y - self.translate[1]) / self.scale[1]
        self.scale = s
        if self.aspect is not None:
            self["scale"] = self.scale * self.aspect
        else:
            self["scale"] = self.scale
        self["translate"] = self.translate
        Transform.on_mouse_scroll(self, x, y, dx, dy)

    def on_mouse_drag(self, x, y, dx, dy, button):
        """ Mouse has been dragged """

        # _, _, width, height = gl.glGetIntegerv(gl.GL_VIEWPORT)
        # FIXME: Why 2* here ?
        #dx =  2*(dx / self.width)
        #dy = -2*(dy / self.height)

        dx =  2*(dx / self.width)
        dy = -2*(dy / self.height)
        self.translate += dx,dy
        self["translate"] = self.translate

        Transform.on_mouse_drag(self, x, y, dx, dy, button)

    def reset(self):
        """ Reset transformation """

        self.scale = np.array([1.,1.])
        self.translate = np.array([0.,0.])
        if self.aspect is not None:
            self["scale"] = np.array([1.,1.]) * self.aspect
        else:
            self["scale"] = np.array([1.,1.])
        self["translate"] = np.array([0.,0.])
