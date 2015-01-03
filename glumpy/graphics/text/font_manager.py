# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import os
import numpy as np
from glumpy import data
from glumpy.log import log
from glumpy.gloo.atlas import Atlas
from glumpy.graphics.text import Font


class FontManager(object):

    # Default atlas
    _atlas = None

    # Font cache
    _cache = {}

    # The singleton instance
    _instance = None


    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    @classmethod
    def get(cls, filename):
        filename = data.get(filename)
        dirname  = os.path.dirname(filename)
        basename = os.path.basename(filename)
        if basename in FontManager._cache.keys():
            return FontManager._cache[basename]
        FontManager._cache[basename] = Font(filename, FontManager._atlas)
        return FontManager._cache[basename]


    # def get_font(self, family, weight=400, stretch='regular', slant='regular'):
    #     log.warn("Not yet implemented")
    #     return self.get_file('')


    @property
    def atlas(self):
        if FontManager._atlas is None:
            FontManager._atlas = np.zeros((1024,1024),np.float32).view(Atlas)
        return FontManager._atlas


    @property
    def cache(self):
        return FontManager._cache
