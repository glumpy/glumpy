#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
from glumpy import library
from glumpy.transforms.transform import Transform


class Translate(Transform):
    """ Translation transform """

    aliases = { "translate" : "translate_translate" }


    def __init__(self, *args, **kwargs):
        code = library.get("transforms/translate.glsl")
        Transform.__init__(self, code, *args, **kwargs)
        self.translate = Transform._get_kwarg("translate", kwargs) or (0,0,0)


    @property
    def translate(self):
        """ Translation """

        return self._translate


    @translate.setter
    def translate(self, value):
        """ Translation """

        self._translate = np.asarray(value,dtype=np.float32)
        if self.is_attached:
            self["translate"] = self._translate


    def on_attach(self, program):
        """ Initialization """

        self["translate"] = self._translate
