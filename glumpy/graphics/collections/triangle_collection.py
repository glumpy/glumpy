# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
""" """
from . raw_triangle_collection import RawTriangleCollection


def TriangleCollection(mode="raw", *args, **kwargs):
    """
    mode: string
      - "raw"  (speed: fastest, size: small,   output: ugly)
      - "agg"  (speed: fast,    size: small,   output: beautiful)
    """

    return RawTriangleCollection(*args, **kwargs)
