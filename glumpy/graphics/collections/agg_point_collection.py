# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
"""
Antigrain Geometry Point Collection

This collection provides fast points. Output quality is perfect.
"""
from glumpy import library, gloo
from . raw_point_collection import RawPointCollection


class AggPointCollection(RawPointCollection):
    """
    Antigrain Geometry Point Collection

    This collection provides fast points. Output quality is perfect.
    """

    def __init__(self, user_dtype=None, transform=None,
                 vertex=None, fragment=None, **kwargs):
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
            fragment= library.get("collections/agg-point.frag")

        RawPointCollection.__init__(self, user_dtype=user_dtype, transform=transform,
                                    vertex=vertex, fragment=fragment, **kwargs)


    def view(self, transform=None):
        vertex = library.get("collections/agg-point.vert")
        fragment= library.get("collections/agg-point.frag")
        saved = vertex
        vertex = ""
        if self.utype is not None:
            vertex += fetchcode(self.utype) + vertex
        else:
            vertex += "void fetch_uniforms(void) { }\n" + vertex
        vertex += self._declarations["uniforms"]
        vertex += self._declarations["attributes"]
        vertex += saved
        program = gloo.Program(vertex, fragment)

        if "transform" in program._hooks.keys():
            if transform is not None:
                program["transform"] = transform
            else:
                program["transform"] = Position3D()

        self._programs.append(program)

        program.bind(self._vertices_buffer)
        for name in self._uniforms.keys():
            program[name] = self._uniforms[name]
        if self._uniforms_list is not None:
            program["uniforms"] = self._uniforms_texture
            program["uniforms_shape"] = self._ushape

        return program
