# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
"""
Viewport transform

The viewport transform allows to restrict the display of a scene to a local
viewport.

The transform is connected to the following events:

 * attach (initialization)
 * resize (update)

Relevant shader code:

 * transforms/viewport.glsl

"""
from glumpy import library
from . transform import Transform


class Viewport(Transform):
    """
    The clipping transform allows to restrict the display of a scene to a local
    viewport.
    """

    aliases = { "clipping"  : "viewport_clipping",
                "transform" : "viewport_transform",
                "local"     : "viewport_local",
                "viewport"  : "viewport_local",
                "global"    : "viewport_global" }


    def __init__(self, code=None, *args, **kwargs):
        """
        Initialize the transform.
        Note that parameters must be passed by name (param=value).

        Kwargs parameters
        -----------------

        transform : bool (default is False)
            Whether to enforce viewport transformation

        clipping : bool (default is False)
            Whether to enforce viewport clipping

        viewport : tuple of 4 floats (default is None)
            Viewport (x,y,w,h) in window coordinates
        """

        if code is None:
            code = library.get("transforms/viewport.glsl")
        self._global = 0,0,512,512
        self._local = Transform._get_kwarg("viewport", kwargs) or None
        self._clipping = Transform._get_kwarg("clipping", kwargs) or True
        self._transform = Transform._get_kwarg("transform", kwargs) or True

        Transform.__init__(self, code, *args, **kwargs)



    @property
    def viewport(self):
        """ Clipping viewport """

        return self._local


    @viewport.setter
    def viewport(self, value):
        """ Clipping viewport """

        self._local = value
        if self.is_attached:
            if self._local is None:
                self["local"] = self._global
            else:
                self["local"] = self._local
            self["clipping"] = self._clipping
            self["transform"] = self._transform


    @property
    def clipping(self):
        """ Whether to enforce viewport clipping """

        return self._clipping


    @clipping.setter
    def clipping(self, value):
        """ Whether to enforce viewport clipping """

        self._clipping = value
        if self.is_attached:
            self["clipping"] = self._clipping


    @property
    def transform(self):
        """ Whether to enforce viewport transform """

        return self._transform


    @transform.setter
    def transform(self, value):
        """ Whether to enforce viewport transform """

        self._transform = value
        if self.is_attached:
            self["transform"] = self._transform



    def on_attach(self, program):
        """ Initialization """

        self["global"] = self._global
        if self._local is None:
            self["local"] = self._global
        else:
            self["local"] = self._local
        self["clipping"] = self._clipping
        self["transform"] = self._transform


    def on_resize(self, width, height):
        """ Update """

        self._global = 0, 0, width, height
        self["global"] = self._global
        if self._local is None:
            self["local"] = self._global

        # Transmit signal to other transforms
        Transform.on_resize(self, width, height)
