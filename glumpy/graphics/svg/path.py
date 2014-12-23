# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import re
import math
from . import arcs, curves
# import arcs, curves

# Minimal distance separating two distinct points
epsilon = 1e-8

def length((x0,y0), (x1,y1)):
    dx, dy = x1-x0, y1-y0
    return math.sqrt(dx*dx+dy*dy)


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
        self.previous = x,y

        return (ox+x,oy+y),



# ------------------------------------------------------------------- VLine ---
class VLine(Command):
    def __init__(self, y=0, relative=True):
        self._command = 'v' if relative else 'V'
        self._args = [y]

    def vertices(self, current, previous=None):
        ox, oy = self.origin(current)
        y = self._args[0]
        self.previous = ox,oy+y

        return (ox,oy+y),


# ------------------------------------------------------------------- HLine ---
class HLine(Command):
    def __init__(self, x=0, relative=True):
        self._command = 'h' if relative else 'H'
        self._args = [x]

    def vertices(self, current, previous=None):
        ox, oy = self.origin(current)
        x = self._args[0]
        self.previous = ox+x,oy

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
        self.previous = current
        return [ ]


# --------------------------------------------------------------------- Arc ---
class Arc(Command):
    def __init__(self, r1=1, r2=1, angle=2*math.pi, large=True, sweep=True,
                 x=0, y=0, relative=True):
        self._command = 'a' if relative else 'A'
        self._args = [r1,r2,angle,large,sweep,x,y]

    def vertices(self, current, previous=None):
        ox, oy = self.origin(current)
        r1,r2,angle,large,sweep,x,y = self._args
        x,y = x + ox, y + oy
        x0,y0 = current
        self.previous = x,y
        segments = elliptical_arc(x0,y0, rx,ry, angle, large, sweep_flag, x, y)
        return segments[1:]


# ------------------------------------------------------------------- Cubic ---
class Cubic(Command):
    def __init__(self, x1=0, y1=0, x2=0, y2=0, x3=0, y3=0, relative=True):
        self._command = 'c' if relative else 'C'
        self._args = [x1,y1,x2,y2,x3,y3]

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
    def __init__(self, x1=0, y1=0, x2=0, y2=0, relative=True):
        self._command = 'q' if relative else 'Q'
        self._args = [x1,y1,x2,y2]

    def vertices(self, current, last_control_point=None):
        ox, oy = self.origin(current)
        x1,y1,x2,y2 = self._args
        x0,y0 = current
        x1,y1 = x1+ox, y1+oy
        x2,y2 = x+ox, y+oy
        self.previous = x1,y1
        segments = curves.quadratic((x0,y0), (x1,y1), (x2,y2))

        return segments[1:]



# ------------------------------------------------------------- SmoothCubic ---
class SmoothCubic(Command):
    def __init__(self, x2=0, y2=0, x3=0, y3=0, relative=True):
        self._command = 's' if relative else 'S'
        self._args = [x2,y2,x3,y3]

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
    def __init__(self, x2=0, y2=0, relative=True):
        self._command = 't' if relative else 'T'
        self._args = [x2,y2]

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

    def __init__(self, description=None):
        # Description of path
        self._paths = []

        # Tesselated path
        self._segments  =[]

        if description:
            self.parse(description)



    def parse(self, description):
        """ Parse an SVG path description """

        commands = re.compile(
            "(?P<command>[MLVHCSQTAZmlvhcsqtaz])(?P<points>[+\-0-9.e, \n\t]*)")

        self._paths = []
        path = []

        for match in re.finditer(commands, description):
            command = match.group("command")
            points = match.group("points").replace(',', ' ')
            points = [float(v) for v in points.split()]
            relative = command in "mlvhcsqtaz"
            command = command.upper()

            while len(points) or command == 'Z':
                if command == 'M':
                    if len(path):
                        self._paths.append(path)
                    path = []
                    path.append( Move(*points[:2], relative=relative) )
                    points = points[2:]
                elif command == 'L':
                    path.append( Line(*points[:2], relative=relative) )
                    points = points[2:]
                elif command == 'V':
                    path.append( VLine(*points[:1], relative=relative) )
                    points = points[1:]
                elif command == 'H':
                    path.append( HLine(*points[:1], relative=relative) )
                    points = points[1:]
                elif command == 'C':
                    path.append( Cubic(*points[:6], relative=relative) )
                    points = points[6:]
                elif command == 'S':
                    path.append( SmoothCubic(*points[:4], relative=relative) )
                    points = points[4:]
                elif command == 'Q':
                    path.append( Quadratic(*points[:4], relative=relative) )
                    points = points[4:]
                elif command == 'T':
                    path.append( SmoothQuadratic(*points[2:], relative=relative) )
                    points = points[2:]
                elif command == 'A':
                    path.append( Arc(*points[:7], relative=relative) )
                    points = points[7:]
                elif command == 'Z':
                    path.append( Close(relative=relative) )
                    self._paths.append(path)
                    path = []
                    break
                else:
                    raise RuntimeError("Unknown SVG path command(%s)" % command)

        if len(path):
            self._paths.append(path)


    def tesselate(self):
        """ Tesselate the path into lists of line segments """

        self._segments = []
        current = 0,0
        previous = 0,0

        for path in self._paths:
            vertices = []
            for command in path:
                V = command.vertices(current, previous)
                previous = command.previous
                vertices.extend( V )
                if len(V) > 0:
                    current = V[-1]
                else:
                    current = 0,0

            if isinstance(command, Close):
                if len(vertices) > 0:
                    if length(vertices[-1], vertices[0]) > epsilon:
                        vertices.append(vertices[0])
                    else:
                        vertices[-1] = vertices[0]

            self._segments.append( vertices )


    def __getitem__(self, key):
        return self._paths[key]


    def __len__(self):
        return len(self._paths)


    @property
    def paths(self):
        return self._paths


    @property
    def segments(self):
        if not len(self._segments):
            self.tesselate()
        return self._segments


    def __repr__(self):
        s = ""
        for path in self.paths:
            for item in path:
                s += repr(item)
        return s



# -----------------------------------------------------------------------------
if __name__ == '__main__':

    path = Path("""m 299.72 80.25 c 0.63 0.18 2.83 1.30 4.08 2.96 c 0.00 0.00 6.80 10.80 1.60 -7.60 c 0.00 0.00 -9.20 -28.80 -0.40 -17.60 c 0.00 0.00 6.00 7.20 2.80 -6.40 c -3.87 -16.43 -6.40 -22.80 -6.40 -22.80 c 0.00 0.00 11.60 4.80 -15.20 -34.80 l 8.80 3.60 c 0.00 0.00 -19.60 -39.60 -41.20 -44.80 l -8.00 -6.00 c 0.00 0.00 38.40 -38.00 25.60 -74.80 c 0.00 0.00 -6.80 -5.20 -16.40 4.00 c 0.00 0.00 -6.40 4.80 -12.40 3.20 c 0.00 0.00 -30.80 1.20 -32.80 1.20 c -2.00 0.00 -36.80 -37.20 -102.40 -19.60 c 0.00 0.00 -5.20 2.00 -9.60 0.80 c 0.00 0.00 -18.40 -16.00 -67.20 6.80 c 0.00 0.00 -10.00 2.00 -11.60 2.00 c -1.60 0.00 -4.40 0.00 -12.40 6.40 c -8.00 6.40 -8.40 7.20 -10.40 8.80 c 0.00 0.00 -16.40 11.20 -21.20 12.00 c 0.00 0.00 -11.60 6.40 -16.00 16.40 l -3.60 1.20 c 0.00 0.00 -1.60 7.20 -2.00 8.40 c 0.00 0.00 -4.80 3.60 -5.60 9.20 c 0.00 0.00 -8.80 6.00 -8.40 10.40 c 0.00 0.00 -1.60 5.20 -2.40 10.00 c 0.00 0.00 -7.20 4.80 -6.40 7.60 c 0.00 0.00 -7.60 14.00 -6.40 20.80 c 0.00 0.00 -6.40 -0.40 -9.20 2.00 c 0.00 0.00 -0.80 4.80 -2.40 5.20 c 0.00 0.00 -2.80 1.20 -0.40 5.20 c 0.00 0.00 -1.60 2.80 -2.00 4.40 c 0.00 0.00 0.80 2.80 -3.60 8.40 c 0.00 0.00 -6.40 18.80 -4.40 24.00 c 0.00 0.00 0.40 4.80 -2.40 6.40 c 0.00 0.00 -3.60 -0.40 4.80 11.60 c 0.00 0.00 0.80 1.20 -2.40 3.60 c 0.00 0.00 -17.20 3.60 -19.60 20.00 c 0.00 0.00 -13.60 14.80 -13.60 20.00 c 0.00 2.31 0.27 5.45 0.97 10.06 c 0.00 0.00 -0.57 8.34 27.03 9.14 c 27.60 0.80 402.72 -31.36 402.72 -31.36 z""")

    V = path.segments[0]
    for i in range(len(V)-1):
        x0,y0 = V[i]
        x1,y1 = V[i+1]
        dx = x1-x0
        dy = y1-y0
        print i,math.sqrt(dx*dx+dy*dy)
