# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
"""
Conic Equal Area projection

See: https://github.com/mbostock/d3/blob/master/src/geo/conic-equal-area.js
     http://mathworld.wolfram.com/AlbersEqual-AreaConicProjection.html
     http://en.wikipedia.org/wiki/Albers_projection
"""
from glumpy import library
from . transform import Transform


class ConicEqualArea(Transform):
    """ Conic Equal Area projection """

    aliases = { "clip"      : "conic_clip",
                "scale"     : "conic_scale",
                "center"    : "conic_center",
                "rotate"    : "conic_rotate",
                "translate" : "conic_translate",
                "parallels" : "conic_parallels" }

    def __init__(self, *args, **kwargs):
        """
        Initialize the transform.
        Note that parameters must be passed by name (param=value).

        Kwargs parameters
        -----------------


        clip : tuple of 4 floats


        scale : float
            Scale factor applied to normalized Cartesian coordinates

        center : float, float
            Center of the projection as (longitude,latitude)

        rotate : float, float, [float]
            Rotation as yaw, pitch and roll.

        translate : float, float
            Translation (in scaled coordinates)

        parallels : float, float
            Parallels as define in conic equal area projection.
        """

        self._clip = Transform._get_kwarg("clip", kwargs, (-180,180,-90,90))
        self._scale = Transform._get_kwarg("scale", kwargs, 1.0)
        self._center = Transform._get_kwarg("center", kwargs, (0,0))
        self._rotate = Transform._get_kwarg("rotate", kwargs, (0,0))
        self._translate = Transform._get_kwarg("translate", kwargs, (0,0))
        self._parallels = Transform._get_kwarg("parallels", kwargs, (0,90))
        code = library.get("transforms/conic-equal-area.glsl")

        # Make sure to call the forward function
        kwargs["call"] = "forward"

        Transform.__init__(self, code, *args, **kwargs)


    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = float(value)
        if self.is_attached:
            self["scale"] = self._scale

    @property
    def clip(self):
        return self._clip

    @clip.setter
    def clip(self, value):
        self._clip = float(value)
        if self.is_attached:
            self["clip"] = self._clip


    @property
    def translate(self):
        return self._translate

    @translate.setter
    def translate(self, value):
        self._translate = float(value)
        if self.is_attached:
            self["translate"] = self._translate

    @property
    def center(self):
        return self._center

    @center.setter
    def center(self, value):
        self._center = value
        if self.is_attached:
            self["center"] = self._center

    @property
    def rotate(self):
        return self._rotate

    @rotate.setter
    def rotate(self, value):
        self._rotate = value
        if self.is_attached:
            self["rotate"] = self._rotate

    @property
    def parallels(self):
        return self._parallels

    @parallels.setter
    def parallels(self, value):
        self._parallels = value
        if self.is_attached:
            self["parallels"] = self._parallels


    def on_attach(self, program):
        """ Initialization event """

        self["clip"] = self._clip
        self["scale"] = self._scale
        self["center"] = self._center
        self["rotate"] = self._rotate
        self["translate"] = self._translate
        self["parallels"] = self._parallels
