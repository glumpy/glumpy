# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
"""
Polar projection

Regular projection using x as rho and y as theta.


The transform is connected to the following events:

 * attach (initialization)

"""
from glumpy import library
from . transform import Transform

class PolarProjection(Transform):
    """ Polar projection """

    aliases = { "origin" : "polar_origin" }

    def __init__(self, *args, **kwargs):
        """
        Initialize the transform.
        Note that parameters must be passed by name (param=value).

        Kwargs parameters
        -----------------

        origin : float (default is 0)
            Angle origin (radians)
        """

        self._origin = Transform._get_kwarg("origin", kwargs) or 0.0
        code = library.get("transforms/polar.glsl")
        Transform.__init__(self, code, *args, **kwargs)



    @property
    def origin(self):
        """ Angle origin (radians) """

        return self._origin


    @origin.setter
    def origin(self, value):
        """ Angle origin (radians) """

        self._origin = float(value)
        if self.is_attached:
            self["origin"] = self._origin


    def on_attach(self, program):
        """ Initialization event """

        self["origin"] = self._origin
