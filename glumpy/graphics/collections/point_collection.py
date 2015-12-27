# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
""" """
from . raw_point_collection import RawPointCollection
from . agg_point_collection import AggPointCollection


def PointCollection(mode="raw", *args, **kwargs):
    """
    mode: string
      - "raw"  (speed: fastest, size: small,   output: ugly)
      - "agg"  (speed: fast,    size: small,   output: beautiful)
    """

    if mode == "raw":
        return RawPointCollection(*args, **kwargs)
    return AggPointCollection(*args, **kwargs)
