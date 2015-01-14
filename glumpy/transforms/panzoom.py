#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
"""
Pan & Zoom transform

The panzoom transform allow to translate and scale an object in the window
space coordinate (2D). This means that whatever point you grab on the screen,
it should remains under the mouse pointer. Zoom is realized using the mouse
scroll and is always centered on the mouse pointer.

The transform is connected to the following events:

 * attach (initialization)
 * resize (update)
 * mouse_scroll (zoom)
 * mouse_grab (pan)

Relevant shader code:

 * transforms/panzoom.glsl

"""
import numpy as np
from glumpy import library
from . transform import Transform


class PanZoom(Transform):
    """ 2D Pan & zoom transform """

    aliases = { "pan"       : "panzoom_translate",
                "translate" : "panzoom_translate",
                "zoom"      : "panzoom_scale",
                "scale"     : "panzoom_scale" }

    def __init__(self, *args, **kwargs):
        """
        Initialize the transform.
        Note that parameters must be passed by name (param=value).

        Kwargs parameters
        -----------------

        aspect : float (default is None)
           Indicate what is the aspect ratio of the object displayed. This is
           necessary to convert pixel drag move in oject space coordinates.

        pan : float, float (default is 0,0)
           Initial translation

        zoom : float, float (default is 1)
           Initial zoom level

        zoom_min : float (default is 0.01)
           Minimal zoom level

        zoom_max : float (default is 1000)
           Maximal zoom level
        """

        code = library.get("transforms/panzoom.glsl")
        Transform.__init__(self, code, *args, **kwargs)

        self._aspect = Transform._get_kwarg("aspect", kwargs) or None
        self._pan = np.array(Transform._get_kwarg("pan", kwargs) or (0.,0.))
        self._zoom_min = Transform._get_kwarg("zoom_min", kwargs) or 0.01
        self._zoom_max = Transform._get_kwarg("zoom_max", kwargs) or 1000
        self._zoom = Transform._get_kwarg("zoom", kwargs) or 1
        self._width = 1
        self._height = 1
        self._window_aspect = np.asarray([1.,1.])


    @property
    def aspect(self):
        """ Aspect (width/height) """

        return self._aspect

    @aspect.setter
    def aspect(self, value):
        """ Aspect (width/height) """

        self._aspect = value


    @property
    def pan(self):
        """ Panning (translation) """
        return self._pan

    @pan.setter
    def pan(self, value):
        """ Panning (translation) """

        self._pan = np.asarray(value)
        if self.is_attached:
            self["pan"] = self._pan


    @property
    def zoom(self):
        """ Zoom level """

        return self._zoom

    @zoom.setter
    def zoom(self, value):
        """ Zoom level """

        self._zoom = np.clip(value, self._zoom_min, self._zoom_max)

        if self.is_attached:
            aspect = 1.0
            if self._aspect is not None:
                aspect = self._window_aspect * self._aspect
            self["zoom"] = self._zoom * aspect


    @property
    def zoom_min(self):
        """ Minimal zoom level """

        return self._zoom_min

    @zoom_min.setter
    def zoom_min(self, value):
        """ Minimal zoom level """

        self._zoom_min = min(value, self._zoom_max)


    @property
    def zoom_max(self):
        """ Maximal zoom level """

        return self._zoom_max

    @zoom_max.setter
    def zoom_max(self, value):
        """ Maximal zoom level """

        self._zoom_max = max(value, self._zoom_min)


    def on_attach(self, program):
        """ Initialization event """

        self["pan"] = self.pan
        aspect = 1.0
        if self._aspect is not None:
            aspect = self._window_aspect * self._aspect
        self["zoom"] = self.zoom * aspect


    def on_resize(self, width, height):
        """ Update event """

        self._width = float(width)
        self._height = float(height)
        aspect = self._width/self._height
        if aspect > 1.0:
            self._window_aspect = np.array([1.0/aspect, 1.0])
        else:
            self._window_aspect = np.array([1.0, aspect/1.0])

        aspect = 1.0
        if self._aspect is not None:
            aspect = self._window_aspect * self._aspect
        self["zoom"] = self.zoom * aspect

        # Transmit signal to other transforms
        Transform.on_resize(self, width, height)


    def on_mouse_scroll(self, x, y, dx, dy):
        """ Zoom event """

        # Normalize mouse coordinates and invert y axis
        x = x/(self._width/2.) - 1.
        y = 1.0 - y/(self._height/2.)

        zoom = np.clip(self._zoom*(1.0+dy/100.0), self.zoom_min, self.zoom_max)
        ratio = zoom / self.zoom
        xpan = x-ratio*(x-self.pan[0])
        ypan = y-ratio*(y-self.pan[1])
        self.zoom = zoom
        self.pan = xpan, ypan


    def on_mouse_drag(self, x, y, dx, dy, button):
        """ Pan event """

        dx =  2*(dx / self._width)
        dy = -2*(dy / self._height)
        self.pan = self.pan + (dx,dy)


    def reset(self):
        """ Reset """

        self.zoom = 1
        self.pan = 0,0
