# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
""" Orthographic projection transform. """
from glumpy import glm, library
from . transform import Transform

class OrthographicProjection(Transform):

    def __init__(self, *args, **kwargs):
        """
        Orthographic projection transform.

        Paremeters
        ----------

        aspect : float (default: None)
            Aspect ratio (width/height) to be enforced

        xinvert: bool (default: False)
            Whether to invert X axis

        yinvert: bool (default: False)
            Whether to invert Y axis

        normalize: bool (default: False)
            Whether to use normalized device coordinates
        """

        code = library.get("transforms/projection.glsl")

        kwargs["aspect"] = kwargs.get("aspect", None)
        self.aspect = kwargs["aspect"]
        del kwargs["aspect"]

        kwargs["xinvert"] = kwargs.get("xinvert", False)
        self.xinvert = kwargs["xinvert"]
        del kwargs["xinvert"]

        kwargs["yinvert"] = kwargs.get("yinvert", False)
        self.yinvert = kwargs["yinvert"]
        del kwargs["yinvert"]

        kwargs["znear"] = kwargs.get("xinvert", -1000)
        self.znear = kwargs["znear"]
        del kwargs["znear"]

        kwargs["zfar"] = kwargs.get("xinvert", +1000)
        self.zfar = kwargs["zfar"]
        del kwargs["zfar"]

        kwargs["normalize"] = kwargs.get("normalize", False)
        self.normalize = kwargs["normalize"]
        del kwargs["normalize"]

        Transform.__init__(self, code, *args, **kwargs)


    def on_resize(self, width, height):
        """ Adjust projection to given size. """

        # Compute new Projection
        xmin, xmax = 0, width
        ymin, ymax = 0, height
        if self.normalize:
            xmin, xmax = -1, +1
            ymin, ymax = -1, +1
        if self.xinvert:
            xmin, xmax = xmax, xmin
        if self.yinvert:
            ymin, ymax = ymax, ymin

        aspect = self.aspect
        if aspect is not None:
            if aspect > 1.0:
                xmin *= (aspect*width)/height
                xmax *= (aspect*width)/height
            else:
                ymin /= (aspect*width)/height
                ymax /= (aspect*width)/height

        znear, zfar = self.znear, self.zfar
        self["projection"] = glm.ortho(xmin, xmax, ymin, ymax, znear, zfar)

        # Propagate event to children
        Transform.on_resize(self, width, height)
