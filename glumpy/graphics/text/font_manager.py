# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
""" Font Manager """
import os
import numpy as np
from glumpy import data
from glumpy.log import log
from glumpy.gloo.atlas import Atlas
from . sdf_font import SDFFont
from . agg_font import AggFont



class FontManager(object):
    """
    Font Manager

    The Font manager takes care of caching already loaded font. Currently, the only
    way to get a font is to get it via its filename. If the font is not available
    on the local data directory, it will be fetched from the font server which
    lives at https://github.com/glumpy/glumpy-font/.
    """

    # Default atlas
    _atlas_sdf = None
    _atlas_agg = None

    # Font cache
    _cache_sdf = {}
    _cache_agg = {}

    # The singleton instance
    _instance = None


    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    @classmethod
    def get(cls, filename, size=12, mode='sdf'):
        """
        Get a font from the cache, the local data directory or the distant server
        (in that order).
        """

        filename = data.get(filename)
        dirname  = os.path.dirname(filename)
        basename = os.path.basename(filename)

        if mode == 'sdf':
            key = '%s' % (basename)
            if FontManager._atlas_sdf is None:
                FontManager._atlas_sdf = np.zeros((1024,1024),np.float32).view(Atlas)
            atlas = FontManager._atlas_sdf
            cache = FontManager._cache_sdf

            if key not in cache.keys():
                cache[key] = SDFFont(filename, atlas)
            return cache[key]

        else: # mode == 'agg':
            key = '%s-%d' % (basename,size)
            if FontManager._atlas_agg is None:
                FontManager._atlas_agg = np.zeros((1024,1024,3),np.ubyte).view(Atlas)

            atlas = FontManager._atlas_agg
            cache = FontManager._cache_agg
            if key not in cache.keys():
                cache[key] = AggFont(filename, size, atlas)
            return cache[key]

    @property
    def atlas_sdf(self):
        if FontManager._atlas_sdf is None:
            FontManager._atlas_sdf = np.zeros((1024,1024),np.float32).view(Atlas)
        return FontManager._atlas_sdf


    @property
    def atlas_agg(self):
        if FontManager._atlas_agg is None:
            FontManager._atlas_agg = np.zeros((1024,1024,3),np.ubyte).view(Atlas)
        return FontManager._atlas_agg
