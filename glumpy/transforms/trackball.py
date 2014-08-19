#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import gl
from glumpy import glm
from glumpy.shaders import get_code
from . transform import Transform
from . import _trackball


class Trackball(Transform):

    def __init__(self, *args, **kwargs):
        #if "code" not in kwargs.keys():
        code = get_code("pvm.glsl")
        Transform.__init__(self, code, *args, **kwargs)

        self._fovy = 30
        self._znear, self._zfar = 2.0, 100.0
        self._trackball = _trackball.Trackball(60,45)
        self._viewport = None
        self._model = self._trackball.model
        self._projection = np.eye(4, dtype=np.float32)
        self._view = np.eye(4, dtype=np.float32)
        glm.translate(self._view, 0, 0, -8)



    def on_attach(self, program):
        program["view"] = self._view
        program["model"] = self._model
        program["projection"] = self._projection


    def on_resize(self, width, height):
        self._viewport = width, height
        self._aspect = width / float(height)
        self['projection'] = glm.perspective(self._fovy, self._aspect,
                                             self._znear, self._zfar)


    def on_mouse_drag(self, x, y, dx, dy, button):
        width, height = self._viewport
        x  = (x*2.0 - width)/width
        dx = (2.*dx)/width
        y  = (height - y*2.0)/height
        dy = -(2.*dy)/height
        self._trackball.drag_to(x,y,dx,dy)

        self._model = self._trackball.model
        self["model"] = self._model


    def on_mouse_scroll(self, x, y, dx, dy):

        self._fovy = np.minimum(np.maximum(self._fovy*(1+dy/100), 10.0), 179.0)
        self['projection'] = glm.perspective(self._fovy, self._aspect,
                                             self._znear, self._zfar)
