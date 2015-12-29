# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
"""
Azimuthal Equidistant projection
"""
from glumpy import library
from . transform import Transform


class AzimuthalEquidistantProjection(Transform):
    """ Azimuthal Equidistant projection """

    aliases = {  }

    def __init__(self, *args, **kwargs):
        """
        Initialize the transform.
        Note that parameters must be passed by name (param=value).

        Kwargs parameters
        -----------------
        """

        code = library.get("transforms/azimuthal-equidistant.glsl")
        Transform.__init__(self, code, *args, **kwargs)


    def on_attach(self, program):
        """ Initialization event """

        pass
