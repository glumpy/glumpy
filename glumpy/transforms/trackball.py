#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
"""
Trackball transform

The trackball transform simulates a virtual trackball (3D) that can rotate
around the origin using intuitive mouse gestures.

The transform is connected to the following events:

 * attach (initialization)
 * resize (update)
 * mouse_scroll (zoom)
 * mouse_grab (pan)

Relevant shader code:

 * transforms/trackball.glsl

"""
import numpy as np
from . import _trackball
from . transform import Transform
from glumpy import glm, library


class Trackball(Transform):
    """ 3D Trackball transform """

    aliases = { "view"       : "trackball_view",
                "model"      : "trackball_model",
                "projection" : "trackball_projection" }

    def __init__(self, *args, **kwargs):
        """
        Initialize the transform.
        Note that parameters must be passed by name (param=value).

        Kwargs parameters
        -----------------

        aspect : float (default is None)
           Indicate what is the aspect ratio of the object displayed. This is
           necessary to convert pixel drag move in oject space coordinates.

        znear : float, float (default is 2)
           Near clip plane

        zfar : float, float (default is 1000)
           Distance clip plane

        theta : float (default is 0)
           Angle (in degrees) around the z axis

        phi:  float (default is 0)
           Angle (in degrees) around the x axis

        distance: float (default is 8)
           Distance from the trackball to the object

        zoom : float (default is 35)
           Zoom level
        """

        code = library.get("transforms/trackball.glsl")
        Transform.__init__(self, code, *args, **kwargs)

        self._aspect = Transform.get("aspect", kwargs) or 1
        self._znear = Transform.get("phi", kwargs) or 2
        self._zfar = Transform.get("theta", kwargs) or 1000
        theta = Transform.get("theta", kwargs) or 0
        phi = Transform.get("phi", kwargs) or 0
        self._distance = Transform.get("zback", kwargs) or 8
        self._zoom = Transform.get("zoom", kwargs) or 35
        self._width = 1
        self._height = 1
        self._window_aspect = np.asarray([1.,1.])

        self._trackball  = _trackball.Trackball(theta, phi)
        self._projection = np.eye(4, dtype=np.float32)
        self._view       = np.eye(4, dtype=np.float32)
        glm.translate(self._view, 0, 0, -abs(self._distance))



    def __getitem__(self, key):
        """ Override getitem to enforce panzoom aliases """

        if key in Trackball.aliases.keys():
            key = Trackball.aliases[key]
        return Transform.__getitem__(self, key)


    def __setitem__(self, key, value):
        """ Override getitem to enforce panzoom aliases """

        if key in Trackball.aliases.keys():
            key = Trackball.aliases[key]
        Transform.__setitem__(self, key, value)


    @property
    def theta(self):
        """ Angle (in degrees) around the z axis """

        return self._trackball.theta

    @theta.setter
    def theta(self, theta):
        """ Angle (in degrees) around the z axis """

        self._trackball.theta = theta
        self["model"] = self._trackball.model


    @property
    def phi(self):
        """ Angle (in degrees) around the x axis """

        return self._trackball.phi

    @phi.setter
    def phi(self, phi):
        """ Angle (in degrees) around the x axis """

        self._trackball.phi = phi
        self["model"] = self._trackball.model


    @property
    def zoom(self):
        """ Zoom level (aperture angle in degrees) """

        return self._zoom


    @phi.setter
    def zoom(self, value):
        """ Angle (in degrees) around the x axis """

        aspect = self._window_aspect * self._aspect
        self._zoom = min(max(value, 1.0), 179.0)
        self['projection'] = glm.perspective(self._zoom, aspect,
                                             self._znear, self._zfar)

    @property
    def aspect(self):
        """ Projection aspect """

        return self._aspect


    @aspect.setter
    def aspect(self, value):
        """ Projection aspect """

        aspect = self._window_aspect * self._aspect
        self['projection'] = glm.perspective(self._zoom, aspect,
                                             self._znear, self._zfar)



    def on_attach(self, program):
        """ Initialization event """

        self["view"] = self._view
        self["model"] = self._trackball.model
        self["projection"] = self._projection


    def on_resize(self, width, height):
        """ Update event """

        self._width  = float(width)
        self._height = float(height)
        self._window_aspect = self._width / self._height
        aspect = self._window_aspect * self._aspect
        self['projection'] = glm.perspective(self._zoom, aspect,
                                             self._znear, self._zfar)

        print self["projection"]

        Transform.on_resize(self, width, height)


    def on_mouse_drag(self, x, y, dx, dy, button):
        """ Drag event """

        width = self._width
        height = self._height
        x  = (x*2.0 - width)/width
        dx = (2.*dx)/width
        y  = (height - y*2.0)/height
        dy = -(2.*dy)/height

        self._trackball.drag_to(x,y,dx,dy)
        self["model"] = self._trackball.model


    def on_mouse_scroll(self, x, y, dx, dy):
        """ Zoom event """

        aspect = self._window_aspect * self._aspect
        self._zoom = min(max(self._zoom*(1-dy/100), 1.0), 179.0)
        self['projection'] = glm.perspective(self._zoom, aspect,
                                             self._znear, self._zfar)
