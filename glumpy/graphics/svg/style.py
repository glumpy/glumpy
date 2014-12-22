# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
from xml.etree import ElementTree

class Style(object):

    def __init__(self, definition):
        self._fill         = None
        self._stroke       = None
        self._parse(definition)


    def _parse(self, definition):
        element = ElementTree.fromstring(definition)

        self._fill = element.get("fill", None)
        self._stroke = element.get("stroke", None)

        print self._fill, self._stroke


style = Style("""
<rect x="400" y="100" width="400" height="200"
      style="fill: yellow" />""")
