# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
"""
Antigrain Geometry Point Collection

This collection provides fast points. Output quality is perfect.
"""
from glumpy import library
from . raw_point_collection import RawPointCollection


class AggPointCollection(RawPointCollection):
    """
    Antigrain Geometry Point Collection

    This collection provides fast points. Output quality is perfect.
    """

    def __init__(self, user_dtype=None, transform=None,
                 viewport=None, vertex=None, fragment=None, **kwargs):
        """
        Initialize the collection.

        Parameters
        ----------

        user_dtype: list
            The base dtype can be completed (appended) by the used_dtype. It
            only make sense if user also provide vertex and/or fragment shaders

        transform: glumpy.Tranforms
            The default vertex shader apply the supplied transform to the
            vertices positions before computing the actual vertices positions
            for path thickness.

        vertex: string
            Vertex shader code

        fragment: string
            Fragment  shader code

        color : string
            'local', 'shared' or 'global'
        """
        if vertex is None:
            vertex = library.get("collections/agg-point.vert")
        if fragment is None:
            fragment = library.get("collections/agg-point.frag")

        RawPointCollection.__init__(self, user_dtype=user_dtype,
                                    transform=transform, viewport=viewport,
                                    vertex=vertex, fragment=fragment, **kwargs)
