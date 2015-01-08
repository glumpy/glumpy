# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
"""
Clipping transform

The clipping transform allows to restrict the display of a scene to a local
viewport.

The transform is connected to the following events:

 * attach (initialization)
 * resize (update)

Relevant shader code:

 * transforms/clipping.glsl
"""
from glumpy import library
from . transform import Transform


class Clipping(Transform):
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

        viewport : tuple of 4 flotas (default is 0,0,1,1)
           Clipped viewport in normalized coordinates
        """

        code = library.get("transforms/clipping.glsl")
        self._viewport = Transform._get_kwarg("viewport", kwargs) or (0,0,256,256)
        Transform.__init__(self, code, *args, **kwargs)


    @property
    def viewport(self):
        """ Clipping viewport """
        return self._viewport


    @viewport.setter
    def viewport(self, value):
        """ Clipping viewport """

        self._viewport = value
        if self.is_attached:
            self["local_viewport"] = self._viewport


    def on_attach(self, program):
        """ Initialization """

        self["local_viewport"] = self._viewport
        self["global_viewport"] = 0, 0, 1, 1


    def on_resize(self, width, height):
        """ Update """

        self["global_viewport"] = 0, 0, width, height

        # Transmit signal to other transforms
        Transform.on_resize(self, width, height)
