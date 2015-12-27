# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
from . raw_path_collection import RawPathCollection
from . agg_path_collection import AggPathCollection
from . agg_fast_path_collection import AggFastPathCollection
#from agg_dash_path_collection  import AggDashPathCollection


def PathCollection(mode="agg", *args, **kwargs):
    """
    mode: string
      - "raw"   (speed: fastest, size: small,   output: ugly, no dash, no thickness)
      - "agg"   (speed: medium,  size: medium   output: nice, some flaws, no dash)
      - "agg+"  (speed: slow,    size: big,     output: perfect, no dash)
      - "agg++" (speed: slowest, size: biggest  output: perfect)
    """

    if mode == "raw":
        return RawPathCollection(*args, **kwargs)
    elif mode == "agg+":
        return AggPathCollection(*args, **kwargs)
    #elif mode.lowercase == "agg-dash":
    #    return AggDashPathCollection(*args, **kwargs)
    return AggFastPathCollection(*args, **kwargs)
