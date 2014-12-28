# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
from glumpy import glm, library
from . transform import Transform

class OrthographicProjection(Transform):

    def __init__(self, *args, **kwargs):
        code = library.get("transforms/projection.glsl")

        kwargs["xinvert"] = kwargs.get("xinvert", False)
        self.xinvert = kwargs["xinvert"]
        del kwargs["xinvert"]

        kwargs["yinvert"] = kwargs.get("yinvert", False)
        self.yinvert = kwargs["yinvert"]
        del kwargs["yinvert"]

        kwargs["znear"] = kwargs.get("xinvert", -1000)
        self.znear = kwargs["znear"]
        del kwargs["znear"]

        kwargs["zfar"] = kwargs.get("xinvert", +1000)
        self.zfar = kwargs["zfar"]
        del kwargs["zfar"]

        Transform.__init__(self, code, *args, **kwargs)

    def on_resize(self, width, height):
        if self.xinvert: xmin,xmax = width,0
        else:            xmin,xmax = 0,width
        if self.yinvert: ymin,ymax = height, 0
        else:            ymin,ymax = 0, height
        znear, zfar = self.znear, self.zfar
        self["projection"] = glm.ortho(xmin, xmax, ymin, ymax, znear, zfar)
        Transform.on_resize(self, width, height)
