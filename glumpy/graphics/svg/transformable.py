# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
from .base import namespace
from .element import Element
from .transform import Transform


class Transformable(Element):
    """ Transformable SVG element """

    def __init__(self, content=None, parent=None):
        Element.__init__(self, content, parent)

        if isinstance(content, str):
            self._transform = Transform()
            self._computed_transform = self._transform
        else:
            self._transform = Transform(content.get("transform",None))
            self._computed_transform = self._transform
            if parent:
                self._computed_transform = self._transform + self.parent.transform

    @property
    def transform(self):
        return self._computed_transform
