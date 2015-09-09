#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
"""
A Color is represented using four normalized channels (red, green, blue and
alpha). Alpha encodes the transparency of the color, with 0 being fully
transparent and 1 being fully opaque.

A single color can be manipulated using the Color object while for sequence of
several color, the Colors object is best.

Example usage:
--------------

color = Color("white")
colors = Colors(["black", "gray", "white"])
"""

from .colors import get
from .color import Color, Colors
