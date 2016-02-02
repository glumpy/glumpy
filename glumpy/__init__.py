# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
__version__ = "1.0.6"

from . import app
from . import api
from . import gloo
from . import data
from . import transforms

from . log import log
from . app import run
from . app import Window
from . app.window import key
from . app.window import mouse

from . graphics import svg
from . graphics import color
from . graphics import collections
