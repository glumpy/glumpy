# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import copy
from glumpy.log import log
from .path import Path
from .style import Style
from .base import namespace
from .element import Element
from .transformable import Transformable


class Group(Transformable):

    def __init__(self, content=None, parent=None):
        Transformable.__init__(self, content, parent)

        self._items = []
        for element in content:
            if not element.tag.startswith(namespace):
                continue
            tag = element.tag[len(namespace):]
            if tag == "g":
                item = Group(element, self)
            elif tag == "path":
                item = Path(element, self)
            else:
                log.warn("Unhandled SVG tag (%s)" % tag)
                continue
            self._items.append(item)


    @property
    def flatten(self):
        i = 0
        L = copy.deepcopy(self._items)
        while i < len(L):
            while isinstance(L[i], Group) and len(L[i]._items):
                L[i:i+1] = L[i]._items
            i += 1
        return L

    @property
    def paths(self):
        return [item for item in self.flatten if isinstance(item,Path)]


    def __repr__(self):
        s = ""
        for item in self._items:
            s += repr(item)
        return s

    @property
    def xml(self):
        return self._xml()

    def _xml(self, prefix=""):
        s = prefix+"<g "
        s += 'id="%s" ' % self._id
        s += self._transform.xml
        s += self._style.xml
        s += ">\n"
        for item in self._items:
            s += item._xml(prefix=prefix+"   ")
        s += prefix+"</g>\n"
        return s
