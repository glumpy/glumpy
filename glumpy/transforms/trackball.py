#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import numpy as np
from . import _trackball
from . transform import Transform
from glumpy import gl, glm, library


class Trackball(Transform):

    def __init__(self, *args, **kwargs):
        code = library.get("transforms/pvm.glsl")
        Transform.__init__(self, code, *args, **kwargs)

        self._fovy = 25
        self._znear, self._zfar = 2.0, 100.0
        self._trackball = _trackball.Trackball(45,45)
        self._viewport = None
        self._model = self._trackball.model
        self._projection = np.eye(4, dtype=np.float32)
        self._view = np.eye(4, dtype=np.float32)
        self._aspect = 1.0
        glm.translate(self._view, 0, 0, -8)


    @property
    def theta(self):
        """ Angle (in degrees) around the z axis """
        return self._trackball.theta

    @theta.setter
    def theta(self, theta):
        self._trackball.theta = theta
        self._model = self._trackball.model
        self["model"] = self._model

    @property
    def phi(self):
        """ Angle (in degrees) around the x axis """
        return self._trackball.phi

    @phi.setter
    def phi(self, phi):
        self._trackball.phi = phi
        self._model = self._trackball.model
        self["model"] = self._model

    @property
    def zoom(self):
        """ Angle (in degrees) around the x axis """
        return self._fovy

    @phi.setter
    def zoom(self, value):
        self._fovy = np.minimum(np.maximum(value, 1.0), 179.0)
        self['projection'] = glm.perspective(self._fovy, self._aspect,
                                             self._znear, self._zfar)



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

        self._fovy = np.minimum(np.maximum(self._fovy*(1-dy/100), 1.0), 179.0)
        self['projection'] = glm.perspective(self._fovy, self._aspect,
                                             self._znear, self._zfar)
