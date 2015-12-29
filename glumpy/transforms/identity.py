# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
from glumpy import library
from . transform import Transform

class IdentityProjection(Transform):
    def __init__(self, *args, **kwargs):
        code = library.get("transforms/position.glsl")
        Transform.__init__(self, code, *args, **kwargs)
