#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
from glumpy.api import matplotlib

figure = matplotlib.Figure()
axes = figure.add_axes([0,0,.5,.5])

figure.show()
