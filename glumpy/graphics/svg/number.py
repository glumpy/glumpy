# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------

class Number(object):

    def __init__(self, content):
        if not content:
            self._value = 0
        else:
            content = content.strip()
            self._value = float(content)

    def __float__(self):
        return self._value

    @property
    def value(self):
        return self._value

    def __repr__(self):
        return repr(self._value)
