# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
from glumpy import library
from . transform import Transform

class Viewport(Transform):

    def __init__(self, *args, **kwargs):
        code = library.get("transforms/viewport.glsl")
        Transform.__init__(self, code, *args, **kwargs)

    def on_attach(self, program):
        """ Initialization event """

        print "Viewport:on_attach"

    def on_resize(self, width, height):

        print "Viewport:on_resize"

        self["viewport"] = 0, 0, width, height

        # Transmit signal to other transforms
        Transform.on_resize(self, width, height)
