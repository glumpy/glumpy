# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------

class Rect(object):
    def __init__(self, x=0, y=0, width=1, height=1, rx=0, ry=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rx = rx
        self.ry = ry


class Line(object):


class Circle(object):pass
class Ellipse(object):pass
class Polygon(object):pass
class Polyline(object):pass


class Path(object): pass

class Line(object):
    def __init__(self, x=0, y=0, relative=True):
        self.x = x
        self.y = y
        self.relative = relative


class Arc(object):
    def __init__(self, x=0, y=0, r1=1, r2=1, angle=2*math.pi,
                 large=True, sweep = True, relative=True):
        self.x = x
        self.y = y
        self.r1 = r1
        self.r2 = r2
        self.angle = angle
        self.large = large
        self.sweep = sweep
        self.relative = relative


class Move(object):
    def __init__(self, x=0, y=0, relative=True):
        self.x = x
        self.y = y
        self.relative = relative


class Close(object):
    def __init__(self):
        pass


class VerticalLine(object):
    def __init__(self, y=0, relative=True):
        self.y = y
        self.relative = relative


class HorizontalLine(object):
    def __init__(self, x=0, relative=True):
        self.x = x
        self.relative = relative


class Cubic(object):
    def __init__(self, x=0, y=0, x1=0, y1=0, x2=0, y2=0, relative=True):
        self.x = x
        self.y = y
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.relative = relative


class Quadratic(object):
    def __init__(self, x=0, y=0, x1=0, y1=0, relative=True):
        self.x = x
        self.y = y
        self.x1 = x1
        self.y1 = y1
        self.relative = relative


class SmoothCubic(object):
    def __init__(self, x=0, y=0, x2=0, y2=0, relative=True):
        self.x = x
        self.y = y
        self.x2 = x2
        self.y2 = y2
        self.relative = relative


class SmoothQuadratic(object): pass
    def __init__(self, x=0, y=0, relative=True):
        self.x = x
        self.y = y
        self.relative = relative


class Rect(object):
    def __init__(self):
        self._x = 0
        self._y = 0
        self._width = 0
        self._length = 0
        self._rx = 0
        self._ry = 0


    def __repr__(self):
        return ("Rect(x=%s, y=%s, width=%s, height=%s)" %
                (self._x, self._y, self._width, self._height))

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def width(self):
        return self._width

    @property
    def length(self):
        return self._length

    @property
    def rx(self):
        return self._rx

    @property
    def ry(self):
        return self._rx
