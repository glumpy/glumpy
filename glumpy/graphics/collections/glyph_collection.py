# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
from . agg_glyph_collection import AggGlyphCollection
from . sdf_glyph_collection import SDFGlyphCollection


def GlyphCollection(mode="sdf", *args, **kwargs):
    """
    mode: string
      - "sdf"   (speed: fast,      size: small, output: decent)
      - "agg"   (speed: fasteest,  size: big    output: perfect)
    """

    if mode == "agg":
        return AggGlyphCollection(*args, **kwargs)
    return SDFGlyphCollection(*args, **kwargs)
