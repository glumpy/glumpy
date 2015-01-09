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

 * transforms/clipping.glsl
"""
from glumpy import library
from . transform import Transform


class Viewport(Transform):
    """
    The clipping transform allows to restrict the display of a scene to a local
    viewport.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the transform.
        Note that parameters must be passed by name (param=value).

        Kwargs parameters
        -----------------

        viewport : tuple of 4 floats (default is None)
           Clipped viewport in normalized coordinates
        """

        code = library.get("transforms/clipping.glsl")
        self._local_viewport = Transform._get_kwarg("viewport", kwargs) or None
        Transform.__init__(self, code, *args, **kwargs)


    @property
    def viewport(self):
        """ Clipping viewport """
        return self._local_viewport


    @viewport.setter
    def viewport(self, value):
        """ Clipping viewport """

        self._local_viewport = value
        if self.is_attached:
            if self._local_viewport is None:
                self["local_viewport"] = self._global_viewport
            else:
                self["local_viewport"] = self._local_viewport


    def on_attach(self, program):
        """ Initialization """

        self["local_viewport"] = self._local_viewport
        self["global_viewport"] = self._global_viewport


    def on_resize(self, width, height):
        """ Update """

        self._global_viewport = 0, 0, width, height
        self["global_viewport"] = self._global_viewport
        if self._local_viewport is None:
            self["local_viewport"] = self._global_viewport


        # Transmit signal to other transforms
        Transform.on_resize(self, width, height)
