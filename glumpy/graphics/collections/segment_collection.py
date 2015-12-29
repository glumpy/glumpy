# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
from . raw_segment_collection import RawSegmentCollection
from . agg_segment_collection import AggSegmentCollection


def SegmentCollection(mode="agg-fast", *args, **kwargs):
    """
    mode: string
      - "raw"      (speed: fastest, size: small,   output: ugly, no dash, no thickness)
      - "agg"      (speed: slower,  size: medium,  output: perfect, no dash)
    """

    if mode == "raw":
        return RawSegmentCollection(*args, **kwargs)
    return AggSegmentCollection(*args, **kwargs)
