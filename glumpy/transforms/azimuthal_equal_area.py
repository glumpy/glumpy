# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
"""
Azimuthal Equal Area projection
"""
from glumpy import library
from . transform import Transform


class AzimuthalEqualAreaProjection(Transform):
    """ Azimuthal Equal Area projection """

    aliases = {  }

    def __init__(self, *args, **kwargs):
        """
        Initialize the transform.
        Note that parameters must be passed by name (param=value).

        Kwargs parameters
        -----------------
        """

        code = library.get("transforms/azimuthal-equal-area.glsl")
        Transform.__init__(self, code, *args, **kwargs)


    def on_attach(self, program):
        """ Initialization event """

        pass
