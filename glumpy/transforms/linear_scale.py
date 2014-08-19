#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
from . import Transform
from glumpy.shaders import get_code


class LinearScale(Transform):
    def __init__(self, *args, **kwargs):
        code = get_code("linear-scale-forward.glsl")
        Transform.__init__(self, code, *args, **kwargs)
