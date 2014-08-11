#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
from glumpy import app

config = app.configuration.Configuration()
config.depth_size = 0
config.api = "GL"
config.srgb = True
print config
print "-----"
window = app.Window(config=config)
print "-----"
print window.config
print "-----"
