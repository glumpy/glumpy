# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
from glumpy import library
from . transform import Transform


class X(Transform):
    def __init__(self, *args, **kwargs):
        code = library.get("transforms/x.glsl")
        Transform.__init__(self, code, *args, **kwargs)

class Y(Transform):
    def __init__(self, *args, **kwargs):
        code = library.get("transforms/y.glsl")
        Transform.__init__(self, code, *args, **kwargs)

class Z(Transform):
    def __init__(self, *args, **kwargs):
        code = library.get("transforms/z.glsl")
        Transform.__init__(self, code, *args, **kwargs)
