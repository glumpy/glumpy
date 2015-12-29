# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
""" This example show how to choose a configuration. """
from glumpy import app

config = app.configuration.Configuration()
config.major_version = 3
config.minor_version = 2
config.profile = "core"
print(config)
print("-----")
window = app.Window(config=config)
print("-----")
print(window.config)
print("-----")
