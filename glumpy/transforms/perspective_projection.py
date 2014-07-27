#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
from glumpy import glm
from . transforms import Transform


class PerspectiveProjection(Transform):

    shaderfile = "projection.glsl"

    def __init__(self, *args, **kwargs):
        Transform.__init__(self, *args, **kwargs)

        self._fovy = 40
        self._znear, self._zfar = 0, 1000
        self._projection = np.eye(4)


    def on_resize(self, width, height):
        fovy = self._fovy
        aspect = width / float(height)
        znear, zfar = self._znear, _zfar
        self["projection"] = glm.perspective(fovy, aspect, znear, zfar)
