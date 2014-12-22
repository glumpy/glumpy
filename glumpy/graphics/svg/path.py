# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import re
import math
import numpy as np
# from . import arcs, curves
import arcs, curves


# -------------------------------------------------------------------- Command ---
class Command(object):
    def __repr__(self):
        s = '%s ' % self._command
        for arg in self._args:
            s += "%.2f " % arg
        return s

    def origin(self, current=None, previous=None):
        relative = self._command in "mlvhcsqtaz"

        if relative and current:
            return current
        else:
            return 0.0,0.0


# -------------------------------------------------------------------- Line ---
class Line(Command):
    def __init__(self, x=0, y=0, relative=True):
        self._command = 'l' if relative else 'L'
        self._args = [x,y]

    def vertices(self, current, previous=None):
        ox, oy = self.origin(current)
        x,y = self._args
        return (ox+x,oy+y),



# ------------------------------------------------------------------- VLine ---
class VLine(Command):
    def __init__(self, y=0, relative=True):
        self._command = 'v' if relative else 'V'
        self._args = [y]

    def vertices(self, current, previous=None):
        ox, oy = self.origin(current)
        y = self._args[0]
        return (ox,oy+y),


# ------------------------------------------------------------------- HLine ---
class HLine(Command):
    def __init__(self, x=0, relative=True):
        self._command = 'h' if relative else 'H'
        self._args = [x]

    def vertices(self, current, previous=None):
        ox, oy = self.origin(current)
        x = self._args[0]
        return (ox+x,oy),


# -------------------------------------------------------------------- Move ---
class Move(Command):
    def __init__(self, x=0, y=0, relative=True):
        self._command = 'm' if relative else 'M'
        self._args = [x,y]

    def vertices(self, current, previous=None):
        ox, oy = self.origin(current)
        x,y = self._args
        x,y = x + ox, y + oy
        self.previous = x,y
        return (x,y),


# ------------------------------------------------------------------- Close ---
class Close(Command):
    def __init__(self, relative=True):
        self._command = 'z' if relative else 'Z'
        self._args = []

    def vertices(self, current, previous=None):
        return [ ]


# --------------------------------------------------------------------- Arc ---
class Arc(Command):
    def __init__(self, x=0, y=0, r1=1, r2=1, angle=2*math.pi,
                 large=True, sweep=True, relative=True):
        self._command = 'a' if relative else 'A'
        self._args = [r1,r2,angle,large,sweep,x,y]

    def vertices(self, current, previous=None):
        ox, oy = self.origin(current)
        x,y,r1,r2,angle,large,sweep = self._args
        x,y = x + ox, y + oy
        x0,y0 = current
        self.previous = x,y
        segments = elliptical_arc(x0,y0, rx,ry, angle, large, sweep_flag, x, y)
        return segments[1:]



# ------------------------------------------------------------------- Cubic ---
class Cubic(Command):
    def __init__(self, x1=0, y1=0, x2=0, y2=0, x=0, y=0, relative=True):
        self._command = 'c' if relative else 'C'
        self._args = [x1,y1,x2,y2,x,y]

    def vertices(self, current, previous=None):
        ox, oy = self.origin(current)
        x0,y0 = current
        x1,y1,x2,y2,x3,y3 = self._args
        x1,y1 = x1+ox, y1+oy
        x2,y2 = x2+ox, y2+oy
        x3,y3 = x3+ox, y3+oy
        self.previous = x2,y2
        segments = curves.cubic((x0,y0), (x1,y1), (x2,y2), (x3,y3))

        return segments[1:]


# --------------------------------------------------------------- Quadratic ---
class Quadratic(Command):
    def __init__(self, x1=0, y1=0, x=0, y=0, relative=True):
        self._command = 'q' if relative else 'Q'
        self._args = [x1,y1,x,y]

    def vertices(self, current, last_control_point=None):
        ox, oy = self.origin(current)
        x1,y1,x,y = self._args
        x0,y0 = current
        x1,y1 = x1+ox, y1+oy
        x2,y2 = x+ox, y+oy
        self.previous = x1,y1
        segments = curves.quadratic(current, (x1,y1), (x2,y2))

        return segments[1:]



# ------------------------------------------------------------- SmoothCubic ---
class SmoothCubic(Command):
    def __init__(self, x2=0, y2=0, x=0, y=0, relative=True):
        self._command = 's' if relative else 'S'
        self._args = [x2,y2,x,y]

    def vertices(self, current, previous):
        ox, oy = self.origin(current)
        x0,y0 = current
        x2,y2,x3,y3 = self._args
        x2,y2 = x2+ox, y2+oy
        x3,y3 = x3+ox, y3+oy
        x1,y1 = 2*x0 - previous[0], 2*y0 - previous[1]
        self.previous = x2,y2
        segments = curves.cubic((x0,y0), (x1,y1), (x2,y2), (x3,y3))

        return segments[1:]


# --------------------------------------------------------- SmoothQuadratic ---
class SmoothQuadratic(Command):
    def __init__(self, x=0, y=0, relative=True):
        self._command = 't' if relative else 'T'
        self._args = [x,y]

    def vertices(self, current, previous):
        ox, oy = self.origin(current)
        x2,y2 = self._args
        x0, y0 = current
        x1,y1 = 2*x0 - previous[0], 2*y0 - previous[1]
        x2, y2 = x2+ox, y2+oy
        self.previous = x1,y1
        segments = curves.quadratic( (x0,y0), (x1,y1), (x2,y2) )

        return segments[1:]


# -------------------------------------------------------------------- Path ---
class Path(object):
    """
    Paths represent the outline of a shape which can be filled, stroked, used
    as a clipping path, or any combination of the three.

    A path is described using the concept of a current point. In an analogy
    with drawing on paper, the current point can be thought of as the location
    of the pen. The position of the pen can be changed, and the outline of a
    shape (open or closed) can be traced by dragging the pen in either straight
    lines or curves.

    Paths represent the geometry of the outline of an object, defined in terms
    of moveto (set a new current point), lineto (draw a straight line), curveto
    (draw a curve using a cubic Bézier), arc (elliptical or circular arc) and
    closepath (close the current shape by drawing a line to the last moveto)
    elements. Compound paths (i.e., a path with multiple subpaths) are possible
    to allow effects such as "donut holes" in objects.
    """

    def __init__(self, expression):
        commands = re.compile(
            "(?P<command>[MLVHCSQTAZmlvhcsqtaz])(?P<points>[+\-0-9.e ]*)")

        self.subpaths = []
        subpath = []

        for match in re.finditer(commands, expression):
            command = match.group("command")
            points = [float(v) for v in match.group("points").split()]
            relative = command in "mlvhcsqtaz"
            command = command.upper()
            if command == 'M':
                if len(subpath):
                    self.subpaths.append(subpath)
                subpath = []
                subpath.append( Move(*points, relative=relative) )
            elif command == 'L':
                subpath.append( Line(*points, relative=relative) )
            elif command == 'V':
                subpath.append( VLine(*points, relative=relative) )
            elif command == 'H':
                subpath.append( HLine(*points, relative=relative) )
            elif command == 'C':
                subpath.append( Cubic(*points, relative=relative) )
            elif command == 'S':
                subpath.append( SmoothCubic(*points, relative=relative) )
            elif command == 'Q':
                subpath.append( Quadratic(*points, relative=relative) )
            elif command == 'T':
                subpath.append( SmoothQuadratic(*points, relative=relative) )
            elif command == 'A':
                subpath.append( Arc(*points, relative=relative) )
            elif command == 'Z':
                subpath.append( Close(relative=relative) )
                self.subpaths.append(subpath)
                subpath = []
            else:
                raise RuntimeError("Unknown SVG path command(%s)" % command)
        if len(subpath):
            self.subpaths.append(subpath)


    @property
    def groups(self):
        """
        """
        groups = []
        current = None
        previous = None

        for subpath in self.subpaths:
            vertices = []
            for i,command in enumerate(subpath):
                V = command.vertices(current, previous)
                previous = command.previous
                vertices.extend( V )
                if len(V) > 0:
                    current = V[-1]
                else:
                    current = None

            groups.append( np.array(vertices) )
        return groups


    def __repr__(self):
        s = ""
        for subpath in self.subpaths:
            for i,part in enumerate(subpath):
                s += repr(part)
        return s

if __name__ == '__main__':
    paths = Path("""M 100 200
                    C 100 100 250 100 250 200
                    S 400 300 400 200
                 """)
    for path in paths.groups:
        print path
