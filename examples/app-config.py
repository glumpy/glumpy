#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
""" This example show how to choose a configuration. """
from glumpy import app

config = app.configuration.Configuration()
config.major_version = 3
config.minor_version = 2
config.profile = "core"
print config
print "-----"
window = app.Window(config=config)
print "-----"
print window.config
print "-----"
