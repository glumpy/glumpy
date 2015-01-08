#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import numpy as np
from . transform import Transform
from glumpy import gl, glm, library


class PVMProjection(Transform):

    def __init__(self, *args, **kwargs):
        code = library.get("transforms/pvm.glsl")
        Transform.__init__(self, code, *args, **kwargs)

        self._fovy = 40
        self._znear, self._zfar = 2.0, 100.0
        self._view = np.eye(4, dtype=np.float32)
        self._model = np.eye(4, dtype=np.float32)
        self._projection = np.eye(4, dtype=np.float32)
        glm.translate(self._view, 0, 0, -5)

    def on_attach(self, program):
        self["view"] = self._view
        self["model"] = self._model
        self["projection"] = self._projection

    def on_resize(self, width, height):
        fovy = self._fovy
        aspect = width / float(height)
        znear, zfar = self._znear, self._zfar
        self['projection'] = glm.perspective(fovy, aspect, znear, zfar)
