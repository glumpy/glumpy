# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import re
import string
from . import arc, curves

class Path(object):

    # ---------------------------------
    def __init__(self):
        self.vertices = []
        self.current = None
        self.last_control3 = None
        self.last_control4 = None

    # ---------------------------------
    def svg_parse(self, cmd, points):
        relative = cmd in string.lowercase
        cmd = string.capitalize(cmd)
        if cmd == 'M':   self.moveto(points,relative)
        elif cmd == 'Z': self.close()
        elif cmd == 'L': self.lineto(points,relative)
        elif cmd == 'H': self.horizontal_lineto(points,relative)
        elif cmd == 'V': self.vertical_lineto(points,relative)
        elif cmd == 'C': self.curveto(points,relative)
        elif cmd == 'Q': self.quadratic_curveto(points,relative)
        elif cmd == 'A': self.elliptical_arc(points, relative)

    # ---------------------------------
    def moveto(self, points, relative = False):
        ox,oy = 0,0
        if len(self.vertices) and len(self.vertices[-1]) <= 1:
            del self.vertices[-1]
        self.vertices.append([])
        vertices = self.vertices[-1]
        x,y = points[:2]
        vertices.append( [x+ox,y+oy] )
        self.current = x+ox,y+oy
        if len(points[2:]):
            self.lineto(points[2:], relative)
        self.current = vertices[-1]
        self.last_control3 = None
        self.last_control4 = None

    # ---------------------------------
    def lineto(self, points, relative = False):
        if relative:
            ox,oy = self.current
        else:
            ox,oy = 0,0
        vertices = self.vertices[-1]
        for i in range(0,len(points),2):
            x,y = points[i],points[i+1]
            vertices.append( [x+ox,y+oy] )
        self.current = vertices[-1]
        self.last_control3 = None
        self.last_control4 = None

    # ---------------------------------
    def horizontal_lineto(self, points, relative=False):
        if relative:
            ox,oy = self.current
        else:
            ox,oy = 0,self.current[1]
        vertices = self.vertices[-1]
        x = points[-1]
        vertices.append( [x+ox,oy] )
        self.current = vertices[-1]
        self.last_control3 = None
        self.last_control4 = None

    # ---------------------------------
    def vertical_lineto(self, points, relative=False):
        if relative:
            ox,oy = self.current
        else:
            ox,oy = self.current[0],0
        vertices = self.vertices[-1]
        y = points[-1]
        vertices.append( [ox,y+oy] )
        self.current = vertices[-1]
        self.last_control3 = None
        self.last_control4 = None

    # ---------------------------------
    def close(self):
        vertices = self.vertices[-1]
        vertices.append( vertices[0] )
        self.last_control3 = None
        self.last_control4 = None

    # ---------------------------------
    def curveto(self, points, relative=False):
        if relative:
            ox,oy = self.current
        else:
            ox,oy = 0,0
        vertices = self.vertices[-1]

        x0, y0 = self.current
        for i in range(0,len(points),6):
            x1,y1 = points[i+0], points[i+1]
            x2,y2 = points[i+2], points[i+3]
            self.last_control4 = x2,y2
            x3,y3 = points[i+4], points[i+5]
            V = curves.curve4_bezier((x0+ox,y0+oy),
                                     (x1+ox,y1+oy),
                                     (x2+ox,y2+oy),
                                     (x3+ox,y3+oy))
            vertices.extend(V[1:].tolist())
            x0,y0 = vertices[-1]
        self.current = vertices[-1]

    # ---------------------------------
    def quadratic_curveto(self, points, relative=False):
        if relative:
            ox,oy = self.current
        else:
            ox,oy = 0,0
        vertices = self.vertices[-1]

        x0, y0 = self.current
        for i in len(0,range(points),4):
            x1,y1 = points[i+0], points[i+1]
            self.last_control3 = x1,y1
            x2,y2 = points[i+2], points[i+3]
            V = curves.curve3_bezier((x0+dx,y0+dy),
                                     (x1+dx,y1+dy),
                                     (x2+dx,y2+dy))
            vertices.extend(V[1:].tolist())
            x0,y0 = vertices[-1]
        self.current = vertices[-1]


    # ---------------------------------
    def smooth_curveto(self, points, relative=False):
        raise NotImplemented

    # ---------------------------------
    def smooth_quadratic_curveto(self, points, relative=False):
        raise NotImplemented

    # ---------------------------------
    def elliptical_arc(self, points, relative=False):
        if relative:
            ox,oy = self.current
        else:
            ox,oy = 0,0
        vertices = self.vertices[-1]

        x0, y0 = self.current
        for i in range(0,len(points),7):
            rx    = points[i+0]
            ry    = points[i+1]
            angle = np.pi*points[i+2]/180.
            large = points[i+3]
            sweep = points[i+4]
            x2    = points[i+5]
            y2    = points[i+6]
            V = arc.elliptical_arc(x0, y0, rx, ry, angle, large, sweep, x2+ox, y2+oy)
            vertices.extend(V[1:].tolist())
            x0,y0 = vertices[-1]
        self.current = vertices[-1]
        self.last_control3 = None
        self.last_control4 = None
