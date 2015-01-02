#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import library
from glumpy.transforms.transform import Transform


class Translate(Transform):
    """
    Translation transform
    """

    def __init__(self, *args, **kwargs):
        code = library.get("transforms/translate-forward.glsl")
        Transform.__init__(self, code, *args, **kwargs)
        self.translate = np.zeros(3,np.float32)


    def on_attach(self, program):
        """ A new program is attached """

        self["translate"] = self.translate
