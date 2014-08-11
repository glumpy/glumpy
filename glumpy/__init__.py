# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
__version__ = "2.0"

from . app import run
from . app import Window

from . app.window import key
from . app.window import mouse
from . graphics.collection import *

from . import app
from . import gloo
from . import data
from . import transforms
from . console import Console
