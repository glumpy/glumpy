# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
from .svg import SVG
from .path import Path
from .base import namespace
from xml.etree import ElementTree

def Document(filename):
    tree = ElementTree.parse(filename)
    root = tree.getroot()
    if root.tag != namespace + 'svg':
        text = 'File "%s" does not seem to be a valid SVG file' % filename
        raise TypeError(text)
    return SVG(root)
